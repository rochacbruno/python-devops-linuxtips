terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Baixar imagem nginx
resource "docker_image" "nginx" {
  name = "nginx:latest"
}

# Criar container
resource "docker_container" "web" {
  name  = "meu-nginx"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = 8080
  }
}
