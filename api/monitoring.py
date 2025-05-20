import graphyte
import os
import psutil
import threading
import time

# Función para inicializar el monitoreo
def init_monitoring(app):
    # Configurar el cliente de Graphite (usando el nombre del servicio en Docker Compose)
    graphyte.init('graphite', 2003, prefix='api.performance')
    
    # Función para enviar métricas de recursos periódicamente
    def send_metrics():
        process = psutil.Process(os.getpid())
        while True:
            try:
                # Métricas de CPU
                cpu_percent = process.cpu_percent(interval=1.0)
                graphyte.send('cpu.percent', cpu_percent)
                
                # Métricas de memoria
                memory_info = process.memory_info()
                memory_percent = process.memory_percent()
                graphyte.send('memory.rss_mb', memory_info.rss / (1024 * 1024))
                graphyte.send('memory.percent', memory_percent)
                
                # Métricas del sistema
                graphyte.send('system.cpu.percent', psutil.cpu_percent())
                graphyte.send('system.memory.percent', psutil.virtual_memory().percent)
                
                # Métricas por endpoint
                endpoints = app.routes
                if hasattr(app, 'endpoint_metrics'):
                    for endpoint, metrics in app.endpoint_metrics.items():
                        if 'calls' in metrics and 'total_time' in metrics:
                            if metrics['calls'] > 0:
                                avg_time = metrics['total_time'] / metrics['calls']
                                graphyte.send(f'endpoints.{endpoint}.avg_time', avg_time)
                                graphyte.send(f'endpoints.{endpoint}.calls', metrics['calls'])
                
                time.sleep(1)  # Intervalo de 1 segundo entre mediciones
            except Exception as e:
                print(f"Error al enviar métricas: {e}")
                time.sleep(5)  # Esperar 5 segundos en caso de error
    
    # Iniciar thread para monitoreo en segundo plano
    metrics_thread = threading.Thread(target=send_metrics, daemon=True)
    metrics_thread.start()
    
    # Inicializar diccionario para métricas de endpoint
    app.endpoint_metrics = {}
    
    # Añadir middleware para monitorear cada solicitud HTTP
    @app.middleware("http")
    async def add_metrics_middleware(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Obtener el nombre del endpoint
        endpoint = request.url.path.replace('/', '_')
        if endpoint.startswith('_'):
            endpoint = endpoint[1:]
        
        # Actualizar métricas para este endpoint
        if endpoint not in app.endpoint_metrics:
            app.endpoint_metrics[endpoint] = {'calls': 0, 'total_time': 0}
        
        app.endpoint_metrics[endpoint]['calls'] += 1
        app.endpoint_metrics[endpoint]['total_time'] += process_time
        
        # Enviar métricas sobre la solicitud HTTP
        graphyte.send(f'http.requests{endpoint}.duration', process_time)
        graphyte.send(f'http.requests{endpoint}.status.{response.status_code}', 1)
        
        return response