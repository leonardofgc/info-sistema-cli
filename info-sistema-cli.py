#!/usr/bin/env python3
"""
Sistema CLI para obter informações do sistema operacional e hardware.
"""
import os
import sys
import platform
import psutil
import argparse
import socket
import json
from datetime import datetime
from tabulate import tabulate

class SystemInfoCli:
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Configura o parser de argumentos da linha de comando"""
        parser = argparse.ArgumentParser(
            description="Ferramenta CLI para obter informações do sistema e hardware",
            epilog="Exemplo: python info-sistema-cli.py --os --cpu --memory"
        )
        parser.add_argument("--os", action="store_true", help="Mostrar informações do sistema operacional")
        parser.add_argument("--cpu", action="store_true", help="Mostrar informações da CPU")
        parser.add_argument("--memory", action="store_true", help="Mostrar informações da memória")
        parser.add_argument("--disk", action="store_true", help="Mostrar informações de disco")
        parser.add_argument("--network", action="store_true", help="Mostrar informações de rede")
        parser.add_argument("--all", action="store_true", help="Mostrar todas as informações")
        parser.add_argument("--json", action="store_true", help="Saída em formato JSON")
        
        return parser
    
    def run(self):
        """Executa a ferramenta CLI"""
        args = self.parser.parse_args()
        
        # Se nenhum argumento for fornecido, mostrar ajuda
        if not any(vars(args).values()):
            self.parser.print_help()
            return
        
        # Coletar informações com base nos argumentos
        info = {}

        if args.os or args.all:
            info['os'] = self.get_os_info()
        
        if args.cpu or args.all:
            info['cpg'] = self.get_cpu_info()
        
        if args.memory or args.all:
            info['memory'] = self.get_memory_info()
        
        if args.disk or args.all:
            info['disk'] = self.get_disk_info()
        
        if args.network or args.all:
            info['network'] = self.get_network_info()
        
        # Exibir as informações
        if args.json:
            self.display_json(info)
        else:
            self.display_formatted(info)
    
    def get_os_info(self):
        """Obtém informações do sistema operacional"""
        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture":platform.architecture()[0],
            "machine":platform.machine(),
            "processor": platform.processor(),
            "hostname":socket.gethostname(),
            "username":os.getlogin() if hasattr(os, 'getlogin') else "N/A",
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
        return info
    
    def get_cpu_info(self):
        """Obtém informações da CPU"""
        cpu_info = {
            "physical_cores":psutil.cpu_count(logical=False),
            "total_cores":psutil.cpu_count(logical=True),
            "max_frequency":f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "N/A",
            "current_frequency": f"{psutil.cpu_freq().current:.2f}" if psutil.cpu_freq() else "N/A",
            "cpu_usage_per_core": [f"{percentage:.2f}" for percentage in psutil.cpu_percent(percpu=True, interval=1)],
            "total_cpu_usage": f"{psutil.cpu_percent()}%"
        }
        return cpu_info
    
    def display_json(self, info):
        """Exibe as informações em formato JSON"""
        print(json.dumps(info, indent=4))
    
if __name__ == "__main__":
    try:
        cli = SystemInfoCli()
        cli.run()
    except KeyboardInterrupt:
        print("\nOperação canelada pelo usuário.")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
    