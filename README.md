AWSAudio
===============================

Play music from your cloud infrastructure 🎼

## Architecture

Since audio in docker is complex, this repository runs a server on your local computer (`FLASK_APP=server python -m flask run -h 0.0.0.0`) listening for connections from your LocalStack instance. Change the IP address in `awsaudio/extension.py` from `192.168.0.10` to the IP address printed in your flask server output.

## Install local development version

To install the extension into localstack in developer mode, you will need Python 3.10, and create a virtual environment in the extensions project.

In the newly generated project, simply run

```bash
make install
```

Then, to enable the extension for LocalStack, run

```bash
localstack extensions dev enable .
```

You can then start LocalStack with `EXTENSION_DEV_MODE=1` to load all enabled extensions:

```bash
EXTENSION_DEV_MODE=1 localstack start
```

## Install from GitHub repository

To distribute your extension, simply upload it to your github account. Your extension can then be installed via:

```bash
localstack extensions install "git+https://github.com/simonrw/awsaudio-extension/#egg=awsaudio"
```
