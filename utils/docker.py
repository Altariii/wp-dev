from ..utils import console

def remove_containers(name_filter: str) -> None:
    console.run_command(f'docker rm $(docker ps -a -q --filter "name={name_filter}")', path='/', shell=True)

def remove_images(name_filter: str) -> None:
    console.run_command(f'docker rmi $(docker images -q --filter "reference={name_filter}")', path='/', shell=True)

def remove_volumes(name_filter: str) -> None:
    console.run_command(f'docker volume rm $(docker volume ls -q --filter "name={name_filter}")', path='/', shell=True)

def remove_project(name: str) -> None:
    remove_containers(name)
    remove_images(name)
    remove_volumes(name)