import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

async def request_cycle(cycle_id: int, disp_id: int):
    '''
    cycle_id: 
    disp_id: 
    Worth mentioning, it expects a mqtt response in the form {disp_id}-{cycle_id}
    return a list of messages in the cyclereqeuest/<disp_id>/response topic
    To be handled outside
    '''
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
                l.append(message.payload.decode())

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
            l = []
            async for message in messages:
                l.append(message.payload.decode())
            return l
