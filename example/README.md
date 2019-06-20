# Example Package

This directory shows an example of the minimum amount of information required for a stub package to be generated.

## Requirements

### For Firmware Modules
* Firmware Folder ([See Here](./micropy-branch))
* Firmware Definition File ([See Here](./micropy-branch/info.jsonc))
  

### For Device
* All Above
* Firmware Version Folder ([See Here](./micropy-branch/v1.0))
* Firmware Device Folder ([See Here](./micropy-branch/v1.0/esp32))
* Device Definition File ([See Here](./micropy-branch/v1.0/esp32/info.json))
* Device Stubs<sup>[1](#device-stubs)</sup> ([See Here](./micropy-branch/v1.0/esp32/stubs))

### Result

If all of the above requirements are met, you should have a directory tree similiar to this:

```sh
 └──     micropy-branch/ 
 │  ├────     info.json  
 │  └────     v1.0/ 
 │  │  └────     esp32/ 
 │  │  │  ├────     info.json  
 │  │  │  └────     stubs/ 
 │  │  │  │  ├────     stub1.py  
 │  │  │  │  └────     stub2.py  
```

Which will then be recognized and have the rest automatically generated as so...

```sh
 └──     micropy-branch/ 
 │  └────     common/ 
 │  │  └────     modules/ 
 │  │  │  ├────     fwaremod1.py  
 │  │  │  └────     fwaremod1.pyi  
 │  ├────     info.json  
 │  └────     v1.0/ 
 │  │  └────     esp32/ 
 │  │  │  ├────     info.json  
 │  │  │  └────     modules/ 
 │  │  │  │  ├────     devicemod1.py  
 │  │  │  │  └────     devicemod1.pyi  
 │  │  │  └────     stubs/ 
 │  │  │  │  ├────     stub1.py  
 │  │  │  │  └────     stub2.py 
```

...with the info.json files updated accordingly.

> <a name="device-stubs">1</a>: As far as I know, the best way to create device stubs is to do it on the actual device using [micropy-cli](https://github.com/BradenM/micropy-cli) or more directly [micropython-stubber](https://github.com/Josverl/micropython-stubber). Therefore, the stubs must be added manually. As I don't own every micropython compatible device, this project will require some PRs for it to be successful. 