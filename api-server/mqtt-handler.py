import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

async def request_cycle(cycle_id, disp_id):
    async with Client("test.mosquitto.org") as client:
        message = "{}-{}".format(disp_id, cycle_id)
        await client.publish(
                "cyclerequest/{}/request".format(disp_id),
                payload=message.encode()
            )
    async with Client("test.mosquitto.org") as client:
        async with client.filtered_messages("cyclerequest/+/response") as messages:
            await client.subscribe("cycleresponse/#")
            async for message in messages:
                return message.payload.decode()

async def return_cycle(cycle_id, disp_id):
    async with Client("test.mosquitto.org") as client:
        message = "{}-{}".format(disp_id, cycle_id)
        await client.publish(
                "cyclereturn/{}/request".format(disp_id),
                payload=message.encode()
            )
    async with Client("test.mosquitto.org") as client:
        async with client.filtered_messages("cyclereturn/+/response") as messages:
            await client.subscribe("cyclereturn/#")
            async for message in messages:
                return message.payload.decode()
