# Larissa Node Dockerfile
This project contains a Dockerfile for setting up a Larissa node inside a Docker container. This guide is based on my personal experience and is intended as a starting point. It might not address all potential issues, and I encourage community contributions to enhance this setup.

## Contributors
- [Santa](https://github.com/Santas-Lair) - Project creator and main developer
- Special thanks to **dark_knight0257** from the [Larissa Discord Server](https://discord.gg/cajyAG6688) for their invaluable contributions and support in the development of this project.

## Prerequsites
You should have a basic understanding of Docker. This setup was tested using Docker Desktop for Windows and has not been tried in other environments.

## Creating a Docker Image

1. Create a work folder.
2. Downlaod the Linux version of Larissa node (geth-ubuntu-x86_64) and place it in the work folder. (from here https://github.com/LarissaBlockchain/Core/releases)
3. Place the dockerfile from this repository in the work folder.
4. Build a docker image by executing the following command in that folder:

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

## Data Persistence

Once your node is created, the running container will utilize a `.ethereum` subfolder within the folder you created for persistent data storage. This folder is where the node stores its operational data. In theory, if the container needs to be rebuilt, it can resume operations using the data from this folder, ensuring continuity without data loss.

### Donations and Referrals

While donations are never required, they are always appreciated if you find this information useful. If you wish to express gratitude, you can send LRS to my wallet at: `0xc6E52ef89173a3655DcF0aCd51e5fB45E0dF9674`.

Additionally, if you are considering purchasing nodes and would like to use my referral code, here it is: `C9S1X4-7669`. Your support helps sustain and improve this project.

