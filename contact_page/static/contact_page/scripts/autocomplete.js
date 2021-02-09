function addautocomplete(identifier, tablename, columnname){
    var tags = [];
    $(identifier).autocomplete({
    source: function (request, response) {
        var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
        response($.grep(tags, function (item) {
            return matcher.test(item);
        }));
        }
    });
    document.querySelector(identifier).onkeyup = function (event) {
        var typed_thing = event.target.value;
        if(typed_thing.length >= 3){
            fetch(`/contact_page/autocomplete_util?table=${tablename}&column=${columnname}&like=` + document.querySelector(identifier).value).then((response) => response.json()).then((response) => {
                tags = [];
                for(const [key, value] of Object.entries(response)){
                    tags.push(value);
                };
            });
        }
    };
}   