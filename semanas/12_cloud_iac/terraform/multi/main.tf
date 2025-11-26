terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Network
resource "docker_network" "app_network" {
  name = "app-network2"
}

# Redis
resource "docker_image" "redis" {
  name = "redis:alpine"
}

resource "docker_container" "redis" {
  name  = "redis"
  image = docker_image.redis.image_id

  networks_advanced {
    name = docker_network.app_network.name
  }
}

# Web App
resource "docker_image" "webapp" {
  name = "nginx:alpine"
}

resource "docker_container" "webapp" {
  name  = "webapp"
  image = docker_image.webapp.image_id

  ports {
    internal = 80
    external = 8081
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

# Output
output "webapp_url" {
  value = "http://localhost:8080"
}
