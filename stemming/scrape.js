$(document).ready(function() {


    var alph = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];



    for(var index = 0; index< alph.length; index++){


        for(var i=0; i<3000; i+=30){
            baseUrl = "http://woordelys.co.za/?alph=" + alph[index] + "&alph_offset="+i;
            $.ajax({
                url: baseUrl,
                type: "get",
                dataType: "",
                success: function(data) {

                    $foop = $('<form>' + data.responseText + '</form>');
                    i =0;

                     $.each($foop.find('div div span span'), function(idx, item) {

                        block = $(item);

                        i++;

                        newText = block.text();

                        
                        newText = newText.replace(/\u2013|\u2014/g, "*");


                        dash_of_index = (newText.indexOf("* of"));

                        if(dash_of_index >-1){
                            newText = newText.substr(0, dash_of_index -1) + " of" + newText.substr(dash_of_index+4);

                        }




                        var words = newText.split("of");
                        newText = "";




                        //sometimes they have random of's between joining words
                        for(var w1 = 0; w1 < words.length; w1++){


                            if(words[w1].length < 4 && w1> 0){

                                words[w1-1] += words[w1-1] + " " + words[w1];
                                words[w1] = "";
                            }



                        }





                        //for each seperated wordd
                        for(var w = 0; w <words.length; w++){
                            words[w] = trim1(words[w]);

                            //add ge.. and ..ge, could generalize later to ..*
                            var dot_index = words[w].indexOf("..ge");

                            var ge_word = "";
                            if(dot_index >-1){
                                change = 0;
                                while(true){
                                    if(words[w].indexOf(words[w][dot_index]) + change < words[w].length && words[w][dot_index +change] != " "){
                                        
                                        ge_word += words[w][dot_index +change];
                                        change++;
                                        //console.log(change);
                                    }else{
                                        break;
                                    }
                                }
                                text_index = (words[w].indexOf(" "));
                                words[w] = words[w].substr(0, dot_index) + words[w].substr(dot_index+ge_word.length+1);

                                insert_index = (words[w].indexOf(ge_word.substr(4)));

                                if(insert_index >-1){
                                    words[w] = words[w].substr(0, text_index)  + ", " + words[w].substr(0, insert_index)+ ge_word.substr(2)  + words[w].substr(text_index);
                                }
                                

                            }




                            dot_index = words[w].indexOf("ge..");

                            ge_word = "e";
                            if(dot_index >-1){
                                change = 0;
                                while(true){
                                    if(words[w].indexOf(words[w][dot_index+2]) - change > 0 && words[w][dot_index -change] != " "){
                                        
                                        ge_word = words[w][dot_index -change] + ge_word;
                                        change++;
                                        //console.log(change);
                                    }else{
                                        break;
                                    }
                                }

                                console.log(ge_word);
                                console.log(words[w]);

                                
                                text_index = (words[w].indexOf(" "));
                                ge_word_index = (words[w].indexOf(ge_word.substr(0, ge_word.length)+".."));

                                words[w] = words[w].substr(0, ge_word_index) + words[w].substr(ge_word_index+ge_word.length +2);


                                
                                insert_index = (words[w].indexOf(ge_word.substr(0, ge_word.length -2)));

                                if(insert_index >-1){
                                    words[w] = words[w].substr(0, text_index)  + ", " + words[w].substr(0, insert_index)+ ge_word  + words[w].substr(insert_index + ge_word.length -2);
                                }
                                
                                

                            }



                            //acount for ge at beggining of words
                            dot_index = words[w].indexOf("ge-");

                            if(dot_index >-1){


                                
                                text_index = (words[w].indexOf(" "));

                                words[w] = words[w].substr(0, dot_index) + words[w].substr(dot_index + 3);



                                words[w] = words[w].substr(0, text_index)  + " ge" + words[w].substr(0, text_index)+ words[w].substr(text_index);

                                
                                

                            }
                            
                            //match plurals -e -s -*
                            text_index = (words[w].indexOf(" "));
                            var re = /(?:^|\W)-(\w+)(?!\w)/g, match, matches = [];
                            while (match = re.exec(words[w])) {
                              matches.push(match[1]);
                            }


                            for(var x =0; x <matches.length; x ++){
                                dash_index = (words[w].indexOf("-"+matches[x]));

                                words[w] = words[w].substr(0, dash_index) + words[w].substr(dash_index+matches[x].length+1);
                                words[w] = words[w].substr(0, text_index)  + ", " + words[w].substr(0, text_index -1)+ matches[x]  + words[w].substr(text_index);

                            }
                            //combine all words seperated by comma's
                            newText += ", " + words[w];


                        
                        }



                            if(block.css("color") === "rgb(33, 45, 122)"){
                                $('<div>'+newText+'</div>').appendTo($('#divs2'));

                            }



                        
                     });
                    

                },
                error: function(status) {
                    //console.log("request error:"+url);
                }


            });

        }

    }

});

function trim1 (str) {
    return str.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
}
