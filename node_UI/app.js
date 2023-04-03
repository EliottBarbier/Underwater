const express = require('express');
const spawn = require('child_process').spawn;
const bodyParser = require('body-parser');

const app = express();

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.render('index');
});

app.post('/', (req, res) => {
  const parametre = req.body.parametre;
  const valeur = req.body.valeur;
  const child = spawn('python', ['camera.py']);

  child.stdin.write(`${parametre}=${valeur}\n`);

  child.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  child.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  child.on('close', (code) => {
    // console.log(`child process exited with code ${code}`);
  });

  res.redirect('/');
});

app.listen(3000, () => {
  console.log('Serveur lancé sur le port 3000');
});
