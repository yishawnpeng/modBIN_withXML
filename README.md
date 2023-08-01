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
   3. ***FF*** User can input {Platfrom} or press enter to use .xml witch first finded

3. Count the value and print it to double check

4. Read write_data.bin which will replace 
   1. ***FF*** User can input 1 to choice other write_data_factory_default.bin otherwise default write_data.bin
   2. ***FF*** User can input manually to modify CT/MAC/ForceNetBoot/counter/timer otherwise default 11002200...EE00/FF..FF/1/5/2
   3. Format : \x00\x00\..\x07 in one line
   4. ***FF*** Support other input format

5. Write date to {Platform_version}.bin
   1. Copy {Platform_version}.bin and rename {Platform_version}_ori.bin then progrm will modify in {Platform_version}.bin

## Installation
1. Clone the repository: ```git clone https://github.com/yishawnpeng/modBIN_withXML.git```
2. Install Python 3.x or later: https://www.python.org/downloads/
3. Install required libraries: ```pip install -r requirements.txt```

## History
For more history information, please reference /history/HISTORY.txt

## How to use
1. Modify target.txt or keep default
2. Modify Write_Data.bin or keep default
3. Run ```modbin_withxml.py``` in cmd window
4. Input which .xml you want to find or press enter to use first finded
5. Input which .bin you want to modify or press enter to use first finded

> Note: Step 1. and 2. can input manully after step 3.

## Contributing
If you would like to contribute to this project, please follow these steps:
 1. Fork the repository
 2. Create a new branch for your feature: ```git checkout -b feature-name```
 3. Make changes and commit them: ```git commit -am 'Add some feature'```
 4. Push to the branch: ```git push origin feature-name```
 5. Submit a pull request