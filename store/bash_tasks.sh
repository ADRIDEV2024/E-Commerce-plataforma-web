analyze_performance() {
    echo "Analizando rendimiento con top y htop..."
    top -n 1 | head -20
    echo "Procesos más pesados:"
    ps aux --sort=-%mem | head -10
}

# 13. Reiniciar aplicación en caso de fallo
auto_restart() {
    echo "Activando reinicio automático en caso de fallo..."
    while true; do
        if ! pgrep -x "my_app" > /dev/null; then
            echo "La aplicación ha fallado, reiniciando..."
            systemctl restart my_app.service
        fi
        sleep 10
    done
}

# 14. Sincronización con servidor remoto
sync_remote() {
    echo "Sincronizando con servidor remoto..."
    rsync -avz --progress ./ usuario@servidor:/ruta/destino
}

start_server() {
    echo "Iniciando servidor de desarrollo..."
    export FLASK_APP=app.py  # Para Flask
    flask run --host=0.0.0.0 --port=5000
}

# 4. Realizar pruebas automatizadas
run_tests() {
    echo "Ejecutando pruebas..."
    pytest tests/  # Para aplicaciones con pytest
}

# 5. Desplegar la aplicación en un servidor
deploy_app() {
    echo "Desplegando aplicación..."
    git pull origin main
    systemctl restart my_app.service  # Reemplazar con el servicio adecuado
}

# 6. Backup y restauración de la base de datos
backup_db() {
    echo "Realizando backup de la base de datos..."
    pg_dump -U usuario -d basededatos > backup.sql
}

restore_db() {
    echo "Restaurando base de datos..."
    psql -U usuario -d basededatos < backup.sql
}
