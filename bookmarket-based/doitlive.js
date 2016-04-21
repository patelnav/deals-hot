current_date = new Date();

toNumber = function(txt) {
    return Number(txt.replace(/[-,]/g, ""));
}

scored_li = new Array();

$.each($('li.threadbit'), function(i,li){
    title = $(li).find("a.title");
    usertxt = $(li).find("a.username.understate").attr("title");
    datetxt = usertxt.split("on ")[1];
    datetxt = datetxt.replace(/st|nd|rd|th/i, "");
    seconds = (current_date - (new Date(datetxt)))/1000;
    replies = toNumber($(li).find("div.threadstats a").text());
    views = toNumber($(li).find("div.threadstats")[1].innerText);
    hits = views + 100 * replies;
    log_score = Math.log10(hits)
    score = log_score - (seconds / 40000)
    //console.log(i, datetxt, replies, views, hits, log_score, score);
    scored_li.push([score, li]);
});

function sortNumber(a,b) {
    return  b[0] - a[0];
}

scored_li.sort(sortNumber);
ol = $("ol#threads");
ol.empty();

$.each(scored_li, function(i, sli){
    $(sli[1]).appendTo(ol);
});
