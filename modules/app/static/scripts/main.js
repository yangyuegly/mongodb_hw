// import { PIL } from "Image";
// import { WordCloud, STOPWORDS, ImageColorGenerator } from "wordcloud";
// import pyplot from "matplotlib";

let formElem = document.getElementById("query-form");
let formElem2 = document.getElementById("histogram-form");

formElem.onsubmit = async (e) => {
  e.preventDefault();

  let response = await fetch("/user", {
    method: "POST",
    body: new FormData(formElem),
  });
  let result = await response.json();

  // var chart = anychart.tagCloud(result);
  var chart = anychart.tagCloud();
  console.log(result);
  chart.data(result, {
    mode: "byWord",
    maxItems: 100,
    ignoreItems: [
      "the",
      "and",
      "he",
      "or",
      "of",
      "in",
      "you",
      "for",
      "with",
      "at",
      "have",
      "its",
      "one",
      "my",
      "there",
      "e",
      "to",
      "a",
      "is",
      "are",
      "on",
      "from",
      "we",
      "this",
      "all",
      "as",
      "it",
      "if",
      "but",
      "1",
      "5",
      "that",
      "house",
      "2",
      "has",
    ],
  });
  // set a chart title
  chart.title("The most frequently appeared words in a summary of a house");
  // set an array of angles at which the words will be laid out
  // enable a color range
  chart.colorRange(false);
  chart.angles([0, -45, 90]);

  // set the color range length
  chart.colorRange().length("80%");
  // display the word cloud chart
  chart.container("container");
  chart.draw();
  // let wordcloud = WordCloud().generate(result);
};

formElem2.onsubmit = async (e) => {
  e.preventDefault();
  let response = await fetch("/user", {
    method: "POST",
    body: new FormData(formElem2),
  });

  var x = [];
  for (var i = 0; i < 500; i++) {
    x[i] = Math.random();
  }

  var trace = {
    x: x,
    type: "histogram",
  };
  var data = [trace];
  Plotly.newPlot("histogram-div", data);
};
