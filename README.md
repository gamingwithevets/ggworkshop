# Basic info
**GGWorkshop** is a Game Genie decoder and encoder written in Python. On **real** Game Genie hardware, some codes may not work correctly, since a real Game Genie can only modify values in **ROM**.  
The tool currently doesn't support *all* platforms (see [Supported Platforms](https://github.com/gamingwithevets/ggworkshop#supported-platforms) for more information).

# Requirements
I recommmend the latest version of Python 3.

# Syntax
```
main.py [-h, --help] [-n, --nologo] [-r, --ramcode] [-a, --autoexit] <option> <platform> <address/code> [<value>] [<condition>]
```
## Parameters
| Parameter | Description |
|--|--|
| `<option>` | Program mode. (`encode/decode`) |
| `<platform>` | Game Genie platform. (`nes/gb/gear/snes/mega`) (note: `gear` = Sega Game Gear, `mega` = Sega Mega Drive/Genesis)
| `<address/code>` | If the `encode` option is used, this is the hex address used for encryption. Must be 2 bytes between $8000 and $FFFF. Must be specified **before** `<value>` and `<condition>`. If the `decode` option is used, this is the code used for decryption. |
| `<value>` | If the `encode` option is used, this is the hex value used for encryption. Must be a 2-digit byte. Must be specified **before** `<address/code>` and **after** `<condition>`. |
| `<condition>` | If the `encode` option is used, this is the conditional hex value used for encryption. Must be a 2-digit byte. If specified, must be **after** `<address/code>` and `<value>`. |
| `-h, --help` | Shows the script help message and exit. |
| `-r, --ramcode` | If the code modifies a value in random-access memory/RAM (`decode` option) or if a RAM address is specified (`encode` option), removes the RAM code warning |
| `-n, --nologo` | Skips the 3-second boot animation when running the script. |
| `-a, --autoexit` | Skips the 10 Enter presses required to exit the program. |

# Usage
Running the script with only the positional arguments will first show this screen (can be disabled with `-n, --nologo`):
![The GGWorkshop boot screen.](https://github.com/gamingwithevets/ggworkshop/raw/main/images/startup.png)
After that, the decoding or encoding process will start. The time it takes depends on the speed of your computer.  
Finally, information about the Game Genie code will be shown, such as the address, value and condition, what the code actually does, etc.  
Here is an example of the screen is shown after the NES Game Genie encoding process:
![GGWorkshop after the NES Game Genie encoding process has completed.](https://github.com/gamingwithevets/ggworkshop/raw/main/images/encode.png)
After that, you are prompted to press Enter 10 times to exit the program (can be disabled with `-a, --autoexit`).

# Supported Platforms
| Platform | **Supported?** | **Can Decode?** | **Can Encode?** | **Supported Versions** |
|--|--|--|--|--|
| Nintendo Entertainment System / NES / Nintendo | **Yes** | **Yes** | **Yes** | **All Versions** |
| Nintendo Game Boy / Game Boy / GB | **Not Fully** | **Yes** | **No** | **v0.3.0+** |
| Sega Game Gear / Game Gear | **Not Fully** | **Yes** | **No** | **v0.3.0+** |
| Super Nintendo Entertainment System / SNES / Super Nintendo | **No** | **No** | **No** | **N/A** |
| Sega Mega Drive / Sega Genesis / Genesis / Mega Drive | **No** | **No** | **No** | **N/A** |

# Examples
To decode and show information about the NES Game Genie code `WALNUT`, type:
```
python main.py decode nes WALNUT
```
To generate an NES Game Genie code that substitutes the value at address $A2D5 with #$69, type:
```
python main.py encode nes A2D5 69
```
To generate an NES Game Genie code that substitutes the value at address $CF70 with #$0C if it's #$0D, type:
```
python main.py encode nes CF70 0C 0D
```
To decode and show information about the Game Boy/Game Gear Game Genie code `123-456-789`, type:
```
python main.py encode nes 123-456-789
```
