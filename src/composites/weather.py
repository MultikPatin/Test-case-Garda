from dishka import AsyncContainer, make_container
from dishka.integrations.fastapi import FastapiProvider

from src.adapters.api import ApiProvider
from src.application.container import make_core_container
from src.application.protocols import MAppProtocol

app = (
    make_container(
        ApiProvider(),
        context={
            AsyncContainer: make_core_container(FastapiProvider()),
        },
    )
    .get(MAppProtocol)
    .api
)
