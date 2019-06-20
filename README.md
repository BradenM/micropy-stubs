# Micropy Stubs

>Note: This is currently a WIP. The end goal is to have a mostly automated
method of creating 'stub packages' with device-specific and firmware-specific
modules included for micropy-cli.

Crawls file tree looking for info.json files,
sorting them by either firmware or device.

If a firmware file is found, it creates the file structure required and downloads/stubs firmware specific modules.

If a device file is found, it will then download its required modules
and stub them. The initial info file and device stubs must be added manually.

Please refer to the [example](./example) directory for more information.


## Credits

This is heavily inspired by (and even uses) [Josvel's micropython-stubber]([https://link](https://github.com/Josverl/micropython-stubber)). All credit for the stub generation in this project goes to him and those who aided him.