# 396bots
Random Snake Generator

This is a program for Assignment 8 for Northwestern University's CS396: Artificial Life

It is heavily based on the ludobots MOOC on https://www.reddit.com/r/ludobots/ created by Professor Josh Bongard

This program runs and generates random creatures in a 3D morphospace in the PyBullet engine. It then evolves these creatures in order to achieve locomotion and incentivizes reproduction of those that travel further.

A diagram of it is attached below

<img width="996" alt="diagramphoto" src="https://user-images.githubusercontent.com/23564433/218646315-534b1151-6549-4756-958c-cb8c8ff0cc95.png">

Morphospace Description:

This leads to a wide potential variety of shapes, and makes it so that blocks can have anywhere from 0 to 6 connected blocks. However, early on a lot oof connections are incentivized and later on fewer connections are incentivzed, making the shape more predictable a lot of the time. Its neurons are also connected in a semi random way, as while each block either has motor/possible sensor neurons, the synapse connections for these are decided randomly, meaning that for example a distant sensor can potentially be linked to a core block motor or vice versa. Movement as of right now is still using the standard pyrosim single joint axis for each joint, but given the potentially large # of blocks it was my opinion that the robot should still be able to have substantial freedom of movement thanks to the vestigial blocks.
To run this program clone this repository and run runsnakemake.py
