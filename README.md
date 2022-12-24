# GameEngine
*2D game engine created during the covid confinement from 2019 to 2021.*

![logo](https://user-images.githubusercontent.com/100092382/209431756-8d32e7f1-8c2e-4172-906d-ac211d741077.png)

This 2D engine is entirely coded in Python.
The goal of this project was to learn as many different concepts as possible through video games.
I supported this engine for 2 years before abandoning its development.
This GitHub folder is just there to show how I coded this project.
Don't expect to be able to run the program easily with the source code, this project is on the long list of "programs that only run on the developer's computer" ;).

The final project is functional but requires many adjustments although the performance is very correct.
Keep in mind that this project was a personal challenge and not intended to become public.
But I thought it would be interesting to share my game engine.

Compatibility is only planned for windows systems (only win10 has been tested).
Despite everything, I strongly invite you to modify my code if you feel like it, it is there for that!
The number of files in this folder is quite substantial due to the many textures used and the lack of optimization of these,
I should have made an image for all the animations of an entity instead of an image each time...

All the textures present in this repo have been drawn by me, yes, it's not always the best and it took me a lot of time.

*Among all the features that I implemented myself, here is a short list.*

**Regarding the game engine itself:**
- Multi-threaded graphical representation to optimize performance.
- Configuration support (see Content/engine.ini).
- Variable window sizes.
- Dynamic window and texture resolution.
- Real-time dynamic frame rate.
- Support for hardware acceleration with OpenGL.
- Sound support with short ambient sounds or long music in real time and asynchronously.
- Surface adaptive footsteps.

**Regarding user events:**
- Full keyboard and mouse support.
- Support for gamepads (Playstation, Xbox).
- Support for Drag and Drop in the graphics window.
- Detection of certain system events such as the reduction of the game window.

**About the game:**
- Game pause menu.
- Quest system.
- Player inventory.
- Management of the player's visual equipment.
- Interaction with game objects or entities.
- Fully complete player animation.
- All game elements are fully animated.
- Presence of NPC or enemy able to follow an entity such as the player or a position.
- Management of different maps with progressive changes and without loading.

**For game map creation:**
- Added building assets, objects, living entity, collision walls, environmental decorations.
- Possibility to change the starting point of the player.
- Map creation statistics.
- Real-time developer tools.
- Management of display layers for assets.
- Map optimization tools.

*And approximately 42 million other things...*

**Here is a small collection of images to present my work:**

![1](https://user-images.githubusercontent.com/100092382/209431784-257801fb-7d1f-4b71-9cda-5e191554894b.png)

**Interaction with NPCs and enemies in the game:**

![2](https://user-images.githubusercontent.com/100092382/209431787-2e3fd695-c920-45f2-a468-6662ca705d88.png)

**Interaction with buildings and objects:**

![3](https://user-images.githubusercontent.com/100092382/209431790-b75117de-9705-4983-ba98-f0b3e7b1bbcf.png)

**Capture of the edit mode of the game map:**

![4](https://user-images.githubusercontent.com/100092382/209431789-a2f31085-4b56-4d19-8849-c8f40f9c6d87.png)
