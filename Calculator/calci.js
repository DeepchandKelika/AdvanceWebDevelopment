//Snippet in catch is repeated multiple times. Can create function to reuse.
//resultBar blinks red for invalid/empty input, green for valid evaluation.
// Anything after '//' is ignored in the input as eval treats it as Javascript comment.

const resultBar = document.getElementById('calculation');
let clearResult = false;

window.onload = function(){
    resultBar.value = '';
}

function appendC(character){

    if( clearResult == true){
        resultBar.value = '';
        clearResult = false;
    }
    resultBar.value += character;

}

function clearResultValue(){
    resultBar.value = '';
}

function evaluateExpression(){

    try{
        if(resultBar.value == ''){
            console.log('Empty');
            throw 'Empty input';
        }
        expression = resultBar.value;
        expression = expression.replace(/\/\/.*/g, '');
        const result = eval(expression); 
        resultBar.value = result;
        clearResult=true;
        blinkResultBar('green');
        
    } catch(exception){
        resultBar.value = '';s
        blinkResultBar('red');
    }
}

function sqrt(){
    try{
    resultBar.value = Math.sqrt(eval(resultBar.value));
    clearResult = true;
    }catch(exception){
        resultBar.value = '';
        blinkResultBar('red');
    }

}


function calTrig(query){
   
   try{
        if(query == 'sin')
            resultBar.value = Math.sin(eval(resultBar.value) * (Math.PI/180)).toFixed(2);
        else if(query == 'cos')
            resultBar.value = Math.cos(eval(resultBar.value)* (Math.PI/180)).toFixed(2);
        else 
            resultBar.value = Math.tan(eval(resultBar.value) * (Math.PI/180)).toFixed(2);

        clearResult = true;
   } catch(exception){
        blinkResultBar('red');
        resultBar.value = '';
   }
}



function blinkResultBar(color) {
    resultBar.style.backgroundColor = color;
    setTimeout(function() {
        resultBar.style.backgroundColor = 'transparent';
    }, 1000);
}