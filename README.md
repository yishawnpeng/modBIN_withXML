# modBIN_withXML
modify bin with location recorded by xml

## Work flow :
1. Can change target.txt to modify more step
   1. Default BiosStartInFullRomImage + PcdFlashNvStorageVariableOffset
   2. Rule : one line of feature-name and one line of act 
   3. The act only suppout +/-
   4. If act isn't correct or feature-name cannot find than it will be skiped

2. Find feature-name which user set in {Platform}.xml
   1. Now can find feature-name in tag of first layer and its text is the value we want
   2. Now can find feature-name in value of "name" tag of forth or fifth layers and the value of the tag "value" of the same layer is what we want
   3. User can choice number or press enter to use .xml witch first finded

3. Count the value and print it to double check

4. Read write_data.bin which will replace 
   1. User can input manually to modify when execution CT/MAC/ForceNetBoot/counter/timer otherwise default 11002200...EE00/FF..FF/1/5/2
   2. User can also modify by command line use parameters
   3. Format for 4-1: \x00\x00\..\x07 in one line
   4. Format for 4-2: number of non-spaced strings from 0-9 and A-F
   5. If use arguments -y it will automatically confirm.
   6. Please note that the BIN file will be modified if the arguments y and the four modification arguments m, s, c, and p are used together

5. Write date to {Platform_version}.bin
   1. Copy {Platform_version}.bin and rename {Platform_version}_ori.bin then progrm will modify in {Platform_version}.bin

## Installation
1. Clone the repository: ```git clone https://github.com/yishawnpeng/modBIN_withXML.git```
2. Install Python 3.x or later: https://www.python.org/downloads/
3. Install required libraries: ```pip install -r requirements.txt```

## History
For more history information, please reference /history/HISTORY.txt

## How to use
1. Modify target.txt if you want to change the location of the bin in the calculation result of .xml or just keep default
2. Modify write_data_default.bin or keep default
3. Put your .xml and .bin in the same folder
4. Run ```M1Inject.exe``` in cmd window and attach the arguments you want to use.
5. Input the corresponding information based on the program's feedback.

> Note: Use ```-h``` if you need more infomateion for arguments 

## Contributing
If you would like to contribute to this project, please follow these steps:
 1. Fork the repository
 2. Create a new branch for your feature: ```git checkout -b feature-name```
 3. Make changes and commit them: ```git commit -am 'Add some feature'```
 4. Push to the branch: ```git push origin feature-name```
 5. Submit a pull request