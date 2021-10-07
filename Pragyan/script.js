function initialFunctioninvestment(){
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("portbutton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
  //change name
  fetch('./stats.json')//has to be http address
  .then(response => response.json())
  .then(data=>{
    console.log(data);

        //Loading data
        document.getElementById("volatility1").innerHTML=data.volatility1;
        document.getElementById("fiveyear1").innerHTML=data.fiveyear1;
        document.getElementById("beta1").innerHTML=data.beta1;
        document.getElementById("treynor1").innerHTML=data.treynor1;
        document.getElementById("jensen1").innerHTML=data.jensen1;
        document.getElementById("var1").innerHTML=data.var1;
        document.getElementById("volatility2").innerHTML=data.volatility2;
        document.getElementById("fiveyear2").innerHTML=data.fiveyear2;
        document.getElementById("beta2").innerHTML=data.beta2;
        document.getElementById("treynor2").innerHTML=data.treynor2;
        document.getElementById("jensen2").innerHTML=data.jensen2;
        document.getElementById("var2").innerHTML=data.var2;
  });

  

}
function tickerUpdate(){
/*


}
*/
}
function initialFunctionportfolio(){
var canvas = document.getElementById("dashboard");
var ctx = canvas.getContext("2d");
ctx.font = "bold 30px Segoe UI ";
ctx.fillText("MY ASSETS", 10, 50);
ctx.fillText("MY ASSETS", 10, 50);
}













/*document.getElementById("volatility1").innerHTML=10;

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("portbutton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function(){
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
*/



/*
var API = require('indian-stock-exchange');
 
var NSEAPI = API.NSE;
var BSEAPI = API.BSE;
 

 
NSEAPI.getIndices()
.then(function (response) { 
  console.log(response.data); //return the api data
});
 
BSEAPI.getIndices()
.then(function (response) { 
  console.log(response.data); //return the api data
});

/*var AlphaVantageAPI = require('alpha-vantage-cli').AlphaVantageAPI;

var apikey = 'IRFC7DNOGKAPIV5G';
var alphaVantageAPI = new AlphaVantageAPI(apikey, 'compact', true);

alphaVantageAPI.getDailyData('BSE:RELIANCE')
    .then(dailyData => {
        console.log("Daily data:");
        console.log(dailyData);
    })
    .catch(err => {
        console.error(err);
    });
*/
