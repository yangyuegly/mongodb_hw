// import { PIL } from "Image";
// import { WordCloud, STOPWORDS, ImageColorGenerator } from "wordcloud";
// import pyplot from "matplotlib";

let formElem = document.getElementById("query-form");
let checkPrice = document.getElementById("find-price");
checkPrice.onclick = async (e) => {
  document.getElementById("container").innerHTML = null;

  e.preventDefault();
  e.stopPropagation();

  let response = await fetch("/country", {
    method: "POST",
    body: new FormData(formElem),
  });
  let result = await response.json();
  google.charts.load("current", { packages: ["corechart"] });
  // google.load("visualization", { packages: ["corechart"] });

  // Set a callback to run when the Google Visualization API is loaded.
  google.charts.setOnLoadCallback(function() {
    var table = new google.visualization.DataTable();

    table.addColumn("string", "Country");
    table.addColumn("number", "Price");
    for (let [key, value] of Object.entries(result)) {
      console.log("key" + key);
      console.log("value" + value);

      table.addRow([key, Math.floor(value)]);
    }

    var price_chart = new google.visualization.BarChart(
      document.getElementById("container")
    );
    price_chart.draw(table);
  });
};

// let formElem2 = document.getElementById("histogram-form");

formElem.onsubmit = async (e) => {
  document.getElementById("container").innerHTML = null;

  e.preventDefault();
  e.stopPropagation();

  let response = await fetch("/user", {
    method: "POST",
    body: new FormData(formElem),
  });
  let result = await response.json();
  var activeElement = document.activeElement;
  let data = [];
  Object.keys(result).forEach(function(key) {
    let curr = {};
    curr["x"] = key;
    curr["value"] = result[key];
    data.push(curr);
  });

  var val = activeElement.value;
  console.log(val);
  if (val == "Show Wordcloud") {
    // var chart = anychart.tagCloud(result);
    var chart = anychart.tagCloud();
    chart.data(data, {
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
        "an",
        "by",
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
    val = "";
  } else if (val == "Show Histogram") {
    document.getElementById("container").innerHTML = null;

    let freqMap = result;
    console.log(result);
    // x.forEach(function(w) {
    //   if (typeof w != "number") {
    //     if (!freqMap[w]) {
    //       freqMap[w] = 0;
    //     }
    //     freqMap[w]++;
    //   }
    // });
    // var trace = {
    //   x: freqMap.keys(),
    //   y: freqMap.values(),
    //   type: "histogram",
    // };

    google.charts.load("current", { packages: ["corechart"] });
    // google.load("visualization", { packages: ["corechart"] });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(function() {
      var data = new google.visualization.DataTable();
      data.addColumn("string", "Word");
      data.addColumn("number", "Frequency");
      stop = [
        "here",
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
        "Here",
        "on",
        "from",
        "we",
        "this",
        "all",
        "as",
        "an",
        "by",
        "it",
        "if",
        "but",
        "1",
        "5",
        "that",
        "house",
        "2",
        "has",
      ];
      for (let [key, value] of Object.entries(freqMap)) {
        key = key
          .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "")
          .replace(/\s+/g, " ");
        if (!stop.includes(key)) {
          // console.log("reached:" + key);
          data.addRow([key.toString(), value]);
        }
      }
      var chart2 = new google.visualization.BarChart(
        document.getElementById("container")
      );
      chart2.draw(data);
    });
  }
};

// formElem2.onsubmit = async (e2) => {
//   e2.preventDefault();
//   let response2 = await fetch("/user", {
//     method: "POST",
//     body: new FormData(formElem2),
//   });
//   let x = await response2.json();

// var options = {
//   title: "Population of Largest U.S. Cities",
//   chartArea: { width: "50%" },
//   colors: ["#b0120a", "#ffab91"],
//   hAxis: {
//     title: "Total Population",
//     minValue: 0,
//   },
//   vAxis: {
//     title: "City",
//   },
// };
