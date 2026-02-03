
//day-1:System understanding
const os = require('os'); 
const fs=require('fs');
const {execSync}=require('child_process'); 

console.log("DAY-1 SYSTEM REPORT");

//makes node take any command as an input and run it on terminal 
function runCommand(cmd) {
    //Exeption handeling to run the commands safely so that the script does not crash
    try{
        return execSync(cmd).toString().trim(); //trim out extra spaces and gives back of the disk
    }catch(e){
        return "Data is not found";
    }
}

//questions the operating system to get it's information metrics
const systemReport={
    "Host Name":os.hostname(),
    "Disk Space":runCommand("df -h / | awk 'NR==2 {print $4}'"),
    "Ports":runCommand("ss -tuln | awk 'NR>1 {print $5}' | cut -d: -f2 | sort -u | head -5").replace(/\n/g, ', '),
    "Gateway":runCommand("ip route | grep default | awk '{print $3}'"),
    "Users":runCommand("who | wc -l")
};
console.table(systemReport); // displays the result in form of a table to get clearer view of the information

const logData={
    timestamp: new Date().toISOString(),
    cpuusageinmicrosec: process.cpuUsage(), 
    resources: process.resourceUsage() 
};

if (!fs.existsSync('./logs')) {
    fs.mkdirSync('./logs');
}

//structured metrics in json format for future analysis
fs.writeFileSync('./logs/day1-sysmetrics.json', JSON.stringify(logData, null, 2)); //makes a file and saves everything in it
console.log("\nInformation is displayed above and log is saved to day1-sysmetrics.json");
