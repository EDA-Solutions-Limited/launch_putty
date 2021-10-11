# launch_putty
<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Putty launcher</h3>

  <p align="center">
    <br />
    <a href="https://github.com/EDA-Solutions-Limited/launch_putty"><strong>Explore the project »</strong></a>
    <br />
    <br />
    <a href="https://github.com/EDA-Solutions-Limited/launch_putty">View Demo</a>
    ·
    <a href="https://github.com/EDA-Solutions-Limited/launch_putty/issues">Report Bug</a>
    ·
    <a href="https://github.com/EDA-Solutions-Limited/launch_putty/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#making-changes">Making changes</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The Tanner Tools are a cross platform tool with the Tanner S-edit tools on the windows side and Mentor Simulator and verification tools hosted on the Linux side. A CAD design engineer needs a quick method to setup their enviroments with little need to consider aspects of the connection between the enviroments and configuration. To provide this smooth experiance for the user a script was devised.

This script aimed to dynamicaly set the users X11 display and launch xming with the correct display settings, dynamicaly obtains the vnc display number and configures putty profile to tunnel 590x from the remote machine to the local machine, and configures the ESXI tool.

### Built With

* [Python](https://www.python.org/)


<!-- GETTING STARTED -->
## Getting Started

To get started with using this code, ensure you have python 3 installed. 

### Prerequisites

The following python libraries are required.
* subprocess
* os
* re
* tempfile
* datetime
* configparser
* winreg
* time
* paramiko
  ```sh
  pip install paramiko
  ```

### Installation

1. Open the project at **..\EDA-Solutions-Limited\launch_putty\launchputty** with an editor.
   Preferrably **vscode**
2. You could also clone the repo
   ```sh
   git clone https://github.com/EDA-Solutions-Limited/launch_putty.git
3. Ensure you edit the createINI function in [**launchputty.py**](https://github.com/EDA-Solutions-Limited/launch_putty/launchputty.py) to your own desired default ini file.

<!-- MAKING CHANGES -->
## Making Changes

<!-- ROADMAP -->
## Roadmap

1. Improve error handling
2. Make Class based
3. change method of detecting display number of vnc

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Not to be distributed to anyone outside EDA solutions. 

<!-- CONTACT -->
## Contact

Henry Frankland - [@hfrank](https://www.linkedin.com/in/henry-frankland-asic/) - henryfrankland@eda-solutions.com - henry@franklandhome.co.uk

Project Link: [launch_putty](https://github.com/EDA-Solutions-Limited/launch_putty.git)
