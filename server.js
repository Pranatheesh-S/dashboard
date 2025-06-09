const express=require('express');
const cors=require('cors');
const { spawn }=require('child_process');
const app=express();
const fs=require('fs');


app.use(cors());
app.use(express.json());
//const python=spawn('python',['reading.py']);

app.post('/update',( req, res )=>{
        const data=req.body.frequency;
        //const python1=spawn('python',['writing.py',data]);
        console.log('frequency has been updated');
        res.json({s:'updated frequency'});
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