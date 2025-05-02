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
    
    def get_memory_info(self):
        """Obtém informações da memória"""
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        memory_info = {
            "total": self._get_size(svmem.total),
            "available": self._get_size(svmem.available),
            "used": self._get_size(svmem.used),
            "percentage":f"{svmem.percent}%",
            "swap_total": self._get_size(swap.total),
            "swap_free": self._get_size(swap.free),
            "swap_used": self._get_size(swap.used),
            "swap_percentage": f"{swap.percent}%"
        }
        return memory_info

    def get_disk_info(self):
        """Obtém informações de disco"""
        try:
            disk_info = {}
            partitions = psutil.disk_partitions()

            for i, partition in enumerate(partitions):
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    disk_info[f"partition_{i}"] = {
                        "device" : partition.device,
                        "mountpoint":partition.mountpoint,
                        "file_system_type":partition.fstype,
                        "total_size": self._get_size(partition_usage.total),
                        "used":self._get_size(partition_usage.used),
                        "free":self._get_size(partition_usage.free),
                        "percentage": f"{partition_usage.percent}%"
                    }
                except PermissionError:
                    disk_info[f"partition_{i}"] = {
                        "device":partition.device,
                        "mountpoint":partition.mountpoint,
                        "file_system_type":partition.fstype,
                        "access":"Sem permissão para ler"
                    }
                # Adicionar informações de IO do disco
                try:
                    disk_io = psutil.disk_io_counters()
                    if disk_io:
                        disk_io["disk_io"] = {
                            "read_since_boot":self._get_size(disk_io.read_bytes),
                            "written_since_boot":self._get_size(disk_io.write_bytes)
                        }
                except(AttributeError, TypeError) as e:
                    disk_info["disk_io_error"] ={
                        "erro": f"Não foi possível obter estatísticas de I/O: {str(e)}"
                    }
                return disk_io
        except Exception as e:
            # Em caso de erro completo, retornar um dicionário com a mensagem de erro
            return {"erro" : f"Erro ao obter informações de disco: {str(e)}"}

    def get_network_info(self):
        """Obtém informações de rede"""
        
        network_info = {
            "interfaces":{}
        }
        
        # Obter endereços IP
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_address in if_addrs.items():
            network_info["interfaces"][interface_name] = []
            for address in interface_address:
                if address.family == socket.AF_INET: # IPv4
                    network_info["interfaces"][interface_name].append({
                        "ip": address.address,
                        "netmask": address.netmask if address.netmask else '-',
                        "broadcast": address.broadcast if address.broadcast else '-'
                    })
                elif address.family == socket.AF_INET6: #IPv6
                    network_info["interfaces"][interface_name].append({
                        "ip": address.address if address.address else '-',
                        "netmask": address.netmask if address.address else '-'
                    })
        # Obter estatísticas de uso da rede
        net_io = psutil.net_io_counters()
        network_info["io_status"] = {
            "bytes_sent":self._get_size(net_io.bytes_sent),
            "bytes_received":self._get_size(net_io.bytes_recv),
            "packets_sent": net_io.packets_sent,
            "packets_received":net_io.packets_recv
        }

        return network_info

    def _get_size(self, bytes_value, suffix = "B"):
        """Converte bytes para um formato legível por humanos"""
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes_value < factor:
                return f"{bytes_value:.2f}{unit}{suffix}"
            bytes_value /= factor
        return f"{bytes_value:.2f}Y{suffix}"

    def display_json(self, info):
        """Exibe as informações em formato JSON"""
        print(json.dumps(info, indent=4))

    def display_formatted(self, info):
         """Exibe as informações formatadas"""
         for section, data in info.items():
            print(f"\n{'=' * 20} {section.upper()} {'=' * 20}")

            if section == 'os':
                self._display_dict_as_table(data)
            elif section == 'cpu':
                cpu_usage = data.pop("cpu_usage_per_core", [])
                self._display_dict_as_tabel(data)
                if cpu_usage:
                    print("\nUso de CPU por núcleo")
                    for i, usage in enumerate(cpu_usage):
                        print(f"Core {i}: {usage}")
            elif section == 'memory':
                self._display_dict_as_table(data)
            elif section == 'disk':
                if isinstance(data, dict):
                    io_stats = None
                    # Separar as estatísticas de I/O
                    if "disk_io" in data:
                        io_stats = data["disk_io"]
                    # Exibir informações das partições
                    for partition_name, partition_data in data.items():
                        if partition_name != "disk_io":
                            print(f"\nPartição: {partition_name}")
                            self._display_dict_as_table(partition_data)
                    
                    # Exibir estatísticas de I/O se disponíveis       
                    if io_stats:
                        print("\nEstatísticas de I/O do Disco")
                        self._display_dict_as_table(io_stats)
                else:
                    # Se data não for um dicionário, exibir diretamente
                    print("\nInformações de Disco:")
                    self._display_dict_as_table(data)
            elif section == 'network':
                interfaces = data.get("interfaces", {})
                for interface_name, addresses in interfaces.items():
                    print(f"Interfaces: {interface_name}")
                    for addr in addresses:
                        self._display_dict_as_table(addr)
                if "io_status" in data:
                    print("\nEstatísticas de I/O de Rede:")
                    self._display_dict_as_table(data["io_status"])

    def _display_dict_as_table(self, data):
        """Exibe um dicionário como uma tabela"""
        if isinstance(data, dict):
            table = [ [key, value] for key, value in data.items() ]
            print(tabulate(table, headers=["Propriedade", "Valor"]))
        else:
            # Para objetos tipo namedtuple ou outros objetos
            try:
                # Tenta converter para dicionário se possível (funciona para namedtuples)
                table = [ [key, getattr(data, key)] for key in dir(data) if not key.startswith('_') and not callable(getattr(data, key))]
                print(tabulate(table, headers=["Propriedade", "Valor"]))
            except Exception:
                print(f"Dados:{data}")
if __name__ == "__main__":
    try:
        cli = SystemInfoCli()
        cli.run()
    except KeyboardInterrupt:
        print("\nOperação canelada pelo usuário.")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
    