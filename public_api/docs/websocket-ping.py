import asyncio
import websockets
import hashlib
import hmac
import json
import time

async def connect():
    async with websockets.connect('wss://exchange.saikungcoffeeandcurry.com/wsapi/v1/live_notifications') as websocket:
        nonce = str(int(round(time.time() * 1000)))
        api_key = 'u0UyKx7zagyMK1cWERyWmSZxWvbjt1Fb'
        secret_key = 'yiifnBFdWHmnLJQ3G8jauZf4l35MXUOe'
        message = api_key + nonce
        signature = hmac.new(
           secret_key.encode(),
           message.encode('utf-8'),
           hashlib.sha256
        ).hexdigest().upper()

        #ping
        await websocket.send('{"command": "ping"}')
        # Wait for server response
        response = await websocket.recv()
        print(response)

#        print('sending....')
#        await websocket.send('{"command":"","params":{},"token":"eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1MTc3MTA1LCJpYXQiOjE2ODUwOTA3MDUsImp0aSI6ImNiZjJkYTQ1MTY0MzRjNTNhNzQ4OTMwNzY5ZDE4ODE5IiwidXNlcl9pZCI6M30.rScPpMEc2jc0wqmY38ki1o9QpHBmFNywPDF8rNOSpW5mugtloafaUoRs30ZhuCZHsclcruX5O17Xw8XWJz-vSg"}')
        # Wait for server response
#        response = await websocket.recv()
#        print(response)
        

        # Construct authentication message
        auth_data = {
            'command': "",
            'params': {},
            'api_key': api_key,
            'signature': signature,
            'nonce': nonce
        }
        # Send authentication message
        print('sending...')
        await websocket.send(json.dumps(auth_data))

        # Wait for server response
        response = await websocket.recv()
        print(response)

        # Send sample messages
        for i in range(5):
            message = {
                'type': 'sample_message',
                'data': {'index': i},
            }
            await websocket.send(json.dumps(message))

            # Wait for server response
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(connect())
