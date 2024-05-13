# Larissa Node Dockerfile
This project contains a Dockerfile for setting up a Larissa node inside a Docker container. This guide is based on my personal experience and is intended as a starting point. It might not address all potential issues, and I encourage community contributions to enhance this setup.

## Prerequsites
You should have a basic understanding of Docker. This setup was tested using Docker Desktop for Windows and has not been tried in other environments.

## Creating a Docker Image

1. Create a work folder.
2. Downlaod the Linux version of Larissa node (geth-ubuntu-x86_64) and place it in the work folder.
3. Place the dockerfile from this repository in the work folder.
4. Build a docker image be executing the following command in that folder:

`docker build -t larissa-node .`

## Creating containers
With the Docker image ready, you can start creating containers:

1. Create an empty folder for your node. I recommend naming this folder after your wallet.
2. Use the command line to run the following command, replacing `[name-for-instance]` with your desired instance name and `YourKey` with your actual user key:
   
`docker run -d --name [name-for-instance1] -v %cd%/.ethereum:/root/.ethereum -e LARISSA_NODE_USER_KEY="YourKey" -p 30303:30303 larissa-node`

Example:

`docker run -d --name Tethys-Ridge-0 -v %cd%/.ethereum:/root/.ethereum -e LARISSA_NODE_USER_KEY="0x71ce168a240f67474b1bcac8896b07822ec89342a78da4c50a608c017618b2d6-RXWB1" -p 30303:30303 larissa-node`

To add additional nodes with different ports:

`docker run -d --name Tethys-Ridge-17 -v %cd%/.ethereum:/root/.ethereum -e LARISSA_NODE_USER_KEY="0x71ce168a240f67474b1bcac8896b07822ec89342a78da4c50a608c017618b2d6-RXWB1" -p 30304:30303 larissa-node`

For Linux bash shell users (untested):

`docker run -d --name larissa-node-instance -v ${PWD}/.ethereum:/app/.ethereum -e LARISSA_NODE_USER_KEY="YourUserKeyHere" -p 30303:30303 larissa-node`

### Donations are never required but always appreciated
However, if you benefit from this information and wish to say thank you, I don't mind if you send a little LRS to my wallet: 0xc6E52ef89173a3655DcF0aCd51e5fB45E0dF9674
If you want to use my referral code when purchasing nodes: C9S1X4-7669

