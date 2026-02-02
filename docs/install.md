# Installation

## Natively

First thing, we need to install some packages

```Bash
sudo apt install build-essential golang-go git yt-dlp ffmpeg libopus-dev -y
```

After installation is done, we can clone the repo with

```Bash
git clone https://github.com/momentodevs/Momento
```

Enter the directory, and build the bot

```Bash
cd Momento
go build
```

We only need to install DCA

```Bash
go get -u github.com/bwmarrin/dca/cmd/dca
```

Final things:
- add `dca` to your path, you can do that by creating a symlink of that executable to your `/usr/bin` directory (`ln -s /home/thetipo01/go/bin/dca /usr/bin/dca`)
- modify the `example_config.yml`, adding all required tokens and renaming it to `config.yml`
- for info about creating and adding the bot, see the following [page](hosting.md)
## Docker

- Clone the repo
- Modify the `example_config.yml`, by adding your discord bot token
  (see [here](hosting.md) if you don't know how to do it)
- Rename it in `config.yml` and move it in the `data` directory
- Run `docker-compose up -d`
- Enjoy your Momento instance!

Note: the docker image is available
on [Docker hub](https://hub.docker.com/r/momentodevs/momento), [Quay.io](https://quay.io/repository/momentodevs/momento)
and [Github packages](https://github.com/momentodevs/Momento/pkgs/container/momento).
