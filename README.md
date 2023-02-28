# 396bots


This is a program for Assignment 8 for Northwestern University's CS396: Artificial Life

It is heavily based on the ludobots MOOC on https://www.reddit.com/r/ludobots/ created by Professor Josh Bongard

This program runs and generates random creatures in a 3D morphospace in the PyBullet engine. It then evolves these creatures in order to achieve locomotion and incentivizes reproduction of those that travel further.

A diagram of it is attached below

![untitled](https://user-images.githubusercontent.com/23564433/221767293-72b6e414-3910-4fe5-81b5-5cb223301285.png)


Morphospace Description:

This leads to a wide potential variety of shapes, and makes it so that blocks can have anywhere from 0 to 6 connected blocks. However, early on a lot of connections are incentivized and later on fewer connections are incentivzed, making the shape more predictable a lot of the time. Its neurons are also connected in a semi random way, as while each block either has motor/possible sensor neurons, the synapse connections for these are decided randomly, meaning that for example a distant sensor can potentially be linked to a core block motor or vice versa. Movement as of right now is still using the standard pyrosim single joint axis for each joint, but given the potentially large # of blocks it was my opinion that the robot should still be able to have substantial freedom of movement thanks to the vestigial blocks.

Fitness:
  Its fitness function is a simple calculation of the x distance of the base block
  
Mutation:
  It randomly decides to add or subtract 1 block(20% chance each), add or subtract 3 blocks (10% chance each), and add or subtract 2 blocks(15% chance each)


To run this program clone this repository and run runsnakemake.py


