const express=require('express');
const cors=require('cors');
const { spawn }=require('child_process');
const app=express();
const fs=require('fs');
let python=null;

app.use(cors());
app.use(express.json());
const python1=spawn('python',['reading.py']);

app.post('/setfrequency',( req, res )=>{
        const data=req.body.frequency;
        const python1=spawn('python',['writing.py',data]);
        console.log(`frequency has been updated${data}`);
        res.json({s:'updated frequency'});
});

app.post('/start',(req,res)=>{
        const register=req.body.register;
        python=spawn('python',['displaying.py',register]);
        console.log('started');
        res.json({message:"start"});
});

app.get('/stop',(req,res)=>{
    if(python==null)
        return res.json({message:"not yet started"});
    python.kill();
    console.log('stopped');
    res.json({message:"stopped"});
});



app.get('/frequency',(req,res)=>{
    fs.readFile('frequency.csv', 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading file:', err);
            return res.status(500).send('Failed to read file.');
        }
         console.log('Read file content:', data);
        res.json({message: data});
    });
});

app.listen(3000,()=>{
    console.log("Server running at http://localhost:3000");
})