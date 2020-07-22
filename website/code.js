var data = JSON.parse(graph);
console.log(data)
console.log(data['nodes'])
var nodes = []
var edges = []

for (i in data['nodes']){
  name = data['nodes'][i]['id']
  let requestURL = 'reddit.com/r/'+name+'/about.json';
  let request = new XMLHttpRequest();
  request.open('GET', requestURL);
  request.responseType = 'json';
  // request.send();
  request.onload = function() {
    const about = request.response;
    nodes.push({
      data: {id: name},
      style:{
        "background-image": 'https://b.thumbs.redditmedia.com/QezhBu7miIfRWmmgBFQ1Fve3ygXz_tgmV5YbMWfEMls.png'
      }

    })

  }

  nodes.push({
    data: {id: name},
    style:{
      "background-image": 'https://b.thumbs.redditmedia.com/QezhBu7miIfRWmmgBFQ1Fve3ygXz_tgmV5YbMWfEMls.png'
    }

  })

}
console.log(nodes)

for (i in data['links']){
  edges.push({data: data['links'][i]})
}
console.log(edges)




var cy = cytoscape({
  container: document.getElementById('cy'),

  boxSelectionEnabled: true,
  autounselectify: true,
  // motionBlur: true,
  // motionBlurOpacity: 0.2,
  wheelSensitivity: 0.1,

  style: cytoscape.stylesheet()
    .selector('node')
      .css({
        'height': 100,
        'width': 100,
        'background-fit': 'cover',
        'border-color': '#4f5b66',
        'border-width': 5,
        'border-opacity': 0.7
      })
      .style({'label':'data(id)'})
    .selector('edge')
      .css({
        'curve-style': 'bezier',
        'width': 6,
        'target-arrow-shape': 'triangle',
        'line-color': '#ffaaaa',
        'target-arrow-color': '#ffaaaa'
      }),
  elements: {
    nodes: nodes,
    edges: edges
  },
  layout: {
    name: 'dagre',
    padding: 10,
    // fit: false,
    // circle: true,
    // maximal: true,
    // roots: '#announcements'
  }
}); // cy init

cy.on('tap', 'node', function(){
  var nodes = this;
  nodes.addClass('selected');
})

// cy.on('tap', 'node', function(){
//   var nodes = this;
//   var tapped = nodes;
//   var food = [];
//
//   nodes.addClass('eater');
//
//   for(;;){
//     var connectedEdges = nodes.connectedEdges(function(el){
//       return !el.target().anySame( nodes );
//     });
//
//     var connectedNodes = connectedEdges.targets();
//
//     Array.prototype.push.apply( food, connectedNodes );
//
//     nodes = connectedNodes;
//
//     if( nodes.empty() ){ break; }
//   }
//
//   var delay = 0;
//   var duration = 500;
//   for( var i = food.length - 1; i >= 0; i-- ){ (function(){
//     var thisFood = food[i];
//     var eater = thisFood.connectedEdges(function(el){
//       return el.target().same(thisFood);
//     }).source();
//
//     thisFood.delay( delay, function(){
//       eater.addClass('eating');
//     } ).animate({
//       position: eater.position(),
//       css: {
//         'width': 10,
//         'height': 10,
//         'border-width': 0,
//         'opacity': 0
//       }
//     }, {
//       duration: duration,
//       complete: function(){
//         thisFood.remove();
//       }
//     });
//
//     delay += duration;
//   })(); } // for
//
// }); // on tap
