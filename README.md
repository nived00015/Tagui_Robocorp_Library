<h1 align="center"><b> TagUI Robocorp Library</b></h1>
<br><br>
<p>Hi all,
This is the library for TagUI Robocorp Integration. TagUI is an open source RPA tool by AI Singapore, a government funded program to accelerate AI. Robocorp is open source RPA tool build on RobotFramework. Using this library, it is possible to write TagUI scripts in Robocorp in different languages.</p>

<h3>To use the library in Robocorp Lab, follow the steps as below: </h3>

Step 1 :  Download the file [<b>Tagui_Robocorp.zip</b>](https://github.com/nived00015/Tagui_Robocorp_Library.git) for understanding the library usage

Step 2 :  From the downloaded zip file, extract the folder [<b>Tagui_Robocorp_Library-main</b>]

Step 3 :  The folder contains <b>tagui_script.py</b>, which is python file and sample robocorp workflow

![image](https://user-images.githubusercontent.com/64367090/114753898-9a46d580-9d75-11eb-95a9-2ca7fa93d83a.png)

Step 4 :  Create a robocorp workflow using Robocorp Lab IDE

Step 5 : After creating the workflow, move/copy the tagui_script.py to the workflow folder with same name [<b>tagui_script.py</b>] as shown below

![image](https://user-images.githubusercontent.com/64367090/114754483-4092db00-9d76-11eb-8adf-f32176c55b59.png)

Step 6 : To use the library features in Robocorp Lab, first import the library in task.robot under Settings cell as <b>tagui_script</b> as below
```
***Settings***
Documentation   Template robot main suite.
Library         tagui_script
````

Step 7 : To execute the TagUI scripts in Robocorp, use <b>Run Script</b> keyword from the <b>tagui_script</b> library
```
***Keywords***
Run English Script
    Run Script
    ...   english
    ...   https://login.xero.com/identity/user/login
    ...   type email as user@gmail.com
    ...   type password as 123456
    ...   click Log In
    ...   echo Logged
```
<b>Run Script</b> keyword takes the following parameters <br>
<b>1. Language</b><br>
<b>2. Tagui Script</b>

<b>Language</b> is the first parameter to <b>Run Script</b> keyword. This tells the keyword in which language tagui script need to be written. In the above example, I am passing the first parameter language as <b>english</b>, since the TagUI script is written in English.

<b>TagUI Script</b> is next parameter need to be passed to the keyword.This is the script which need to be automated. Here tagui script is written as line by line. As seen in above example, the tagui script is for automation of login to a website by entering username and password and output the <b>Logged</b> word after login.It is written line by line after the parameter <b>english</b>.

Just run the process and you will see the results like this

![image](https://user-images.githubusercontent.com/64367090/114763138-19410b80-9d80-11eb-9f3b-848eb60e6ce5.png)

It is seen as it had output the word <b>Logged</b>

<h3 align="center"><b>Congratulations on your first tagui script ran successfully on Robocorp :heart_eyes:🎉🎉:robot:</b></h3><br><br>

<b>I hope you had got an idea on how the library works......</b><br><br>

<h3 align="center"><b>Let's explore some additional concepts............</b></h3><br>

<b>1. Adding the output of tagui script to a variable</b>

Sometimes it is required to store the output of tagui process to be used for other purpose in automation process thus linking the tagui process with Robocorp. The TagUI Robocorp Library store the output of the tagui process in a form of list, which contains the output of TagUI process.

For eg, a TagUI Script is written for calculation of forex rates and finally it will output the value of forex rate conversion. 

<b>TagUI Script</b>
```
*** Keywords ***
Run English
     ${output}=  Run Script 
    
    ...  english
    ...  https://www.calculator.net/currency-calculator.html
    ...  ask enter The currency u need to know
    ...  type //input[@type="text"] as [clear] 1
    ...  select //select[@name="efrom"] as `ask_result`
    ...  select //select[@name="eto"] as INR
    ...  click //input[@value="Calculate"]
    ...  read //font[@color="green"] to data
    ...  echo ONE AUD is equal to `data` INR
    
    Notebook Print  output via Robocorp is ${output}
```

As you see in the code, The output of keyword <b>Run Script</b> should be stored in <b>${output}</b> variable, which is a list. At last, <b>Notebook Print</b> is used to print the ${output} variable as <b>output via Robocorp is ${output}</b> so to understand the output via Notebook Print [since there would be output from the Run Script keyword too]

<b>Output of above code</b><br><br>
![image](https://user-images.githubusercontent.com/64367090/115036688-5c6bbd80-9eeb-11eb-9c11-08886585bec1.png)

So you can see that , the first line output is coming defaulty when Run Script keyword runs, while the second line output <b>output via Robocorp is ['ONE AUD is equal to 89.22766 INR']</b> is done by Notebook Print, and we can see that <b>${output}</b> variable is a list here <b>['ONE AUD is equal to 89.22766 INR']</b>. Now we can even loop through this and do the required logic for the process.<br><br>



<b>2. Writing TagUI Script in Robocorp in different languages</b><br>

So far, we had seen writing TagUI script written in English language in Robocorp, it is possible to write in other languages too. Refer the below code examples for writing TagUI Script using <b>Run Script</b> keyword in different languages by changing the <b>Language</b> parameter. 

<b>Hindi</b>
```
***Keywords***
Run Hindi
    Run Script
    ...  hindi
    ...  https://login.xero.com/identity/user/login
    ...  लिखो email जैसा user@gmail.com
    ...  लिखो password जैसा 12345678
    ...  क्लिक Log in    
```

<b>Chinese</b>
```
***Keywords***
Run Chinese
    Run Script
    ...  chinese
    ...  https://login.xero.com/identity/user/login
    ...  输入 email 为 user@gmail.com
    ...  输入 password 为 12345678
    ...  点击 Log in
```

<b>Russian</b>
```
***Keywords***
Run Russian
    Run Script
    ...  russian
    ...  https://login.xero.com/identity/user/login
    ...  тип email в виде user@gmail.com
    ...  тип password в виде 12345678
    ...  щелчок Log in
```
<br><br>

<h3> For More Details........</h3>

[Library working demo](https://youtu.be/HAfQpNZVbKI)

[LinkedIn Announcement](https://www.linkedin.com/posts/nived-n-776470139_nived00015taguirobocorplibrary-activity-6787800490831962112-8-wz)
