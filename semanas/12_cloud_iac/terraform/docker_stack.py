#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_docker.provider import DockerProvider
from cdktf_cdktf_provider_docker.image import Image
from cdktf_cdktf_provider_docker.container import Container, ContainerPorts


class DockerStack(TerraformStack):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        # Provider
        DockerProvider(self, "docker")

        # Imagem Nginx
        nginx_image = Image(self, "nginx-image",
            name="nginx:latest",
            # keep_locally=False
        )

        # Container
        Container(self, "nginx-container",
            name="my-nginx",
            image=nginx_image.image_id,
            ports=[ContainerPorts(
                internal=80,
                external=8082
            )]
        )


app = App()
DockerStack(app, "cdktf-docker")
app.synth()

