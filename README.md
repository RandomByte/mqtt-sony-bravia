# mqtt-sony-bravia

[![Docker Hub Pulls](https://img.shields.io/docker/pulls/randombyte/armhf-mqtt-sony-bravia.svg)](https://hub.docker.com/r/randombyte/armhf-mqtt-sony-bravia)

Poll the [HTTP endpoint](https://gist.github.com/kalleth/e10e8f3b8b7cb1bac21463b0073a65fb) of a legacy (pre-Android) Sony Bravia TVs for various information and publish those via MQTT

## Usage
mqtt-sony-bravia can be configured using environment variables:

- **MQTT_SB_TV_IP:** IP of your Sony Bravia TV in your network
- **MQTT_SB_MQTT_BROKER:** IP or hostname of your MQTT broker
- **MQTT_SB_MQTT_TOPIC_PREFIX:** MQTT topic prefix to publish TV status information on, e.g. `Home/TV/` (must end with a slash)

## Docker Image
A Docker image for the **armhf** architecture (Raspberry Pi et al.) is available on [Docker Hub](https://hub.docker.com/r/randombyte/armhf-mqtt-traffic).

## Example

### Option 1: Docker
````sh
docker run --rm -it \
MQTT_SB_TV_IP="<IP of TV>" \
MQTT_SB_MQTT_BROKER="<broker HOST or IP>" \
MQTT_SB_MQTT_TOPIC_PREFIX="Home/TV/" \
randombyte/armhf-sony-bravia:latest
````

### Option 2: Source
````sh
MQTT_SB_TV_IP="<IP of TV>" \
MQTT_SB_MQTT_BROKER="<broker HOST or IP>" \
MQTT_SB_MQTT_TOPIC_PREFIX="Home/TV/" \
python3 src/main.py
````

### MQTT Message Examples

| Topic        | Payload
| ------------- |-------------|
| `Home/TV/Connections/hdmi1` | `Connected` |
| `Home/TV/Connections/hdmi2` | `Disconnected` |
| `Home/TV/Connections/av1` | `Disconnected` |
| `Home/TV/Connections/player1` | `Disconnected` |
| `Home/TV/Connections/player2` | `Connected` |

## License
Released under the [MIT License](https://opensource.org/licenses/MIT).
