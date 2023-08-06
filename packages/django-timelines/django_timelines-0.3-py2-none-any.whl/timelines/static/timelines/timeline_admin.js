(function($) {
    function myEscape(value) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(value));
        return div.innerHTML;
    }
    function setHints(data) {
        $('.field-headline_ovr .help').html(myEscape(data.headline));
        $('.field-text_ovr .help').html(myEscape(data.text));
        $('.field-caption_ovr .help').html(myEscape(data.caption));
        $('.field-credit_ovr .help').html(myEscape(data.credit));
    }

    function relatedObjectSelected() {
        var ctype_id = $('#id_content_type')[0].value,
            obj_id = $('#id_object_id')[0].value;

        return $.isNumeric(ctype_id) && $.isNumeric(obj_id);
    }
    function getAdapterValues(e) {
        if (relatedObjectSelected()) {
            var path = window.location.pathname.split('/').slice(0, -2).join('/'),
                ctype = django.jQuery('#id_content_type')[0].value,
                obj_id = django.jQuery('#id_object_id')[0].value,
                defaultHints = {
                    headline: "This object doesn't provide a headline. Provide a headline above.",
                    text: "This object doesn't provide text. Provide text above.",
                    caption: "This object doesn't provide a caption. Provide a caption above.",
                    credit: "This object doesn't provide credit. Provide a credit above. "
                };
            path += '/adapter_fields/' + ctype + '/' + obj_id + '/';

            $.get(path, {}, function(data){
                if (data.headline)
                    defaultHints.headline = "DEFAULT: " + data.headline;
                if (data.text)
                    defaultHints.text = "DEFAULT: " + data.text;
                if (data.caption)
                    defaultHints.caption = "DEFAULT: " + data.caption;
                if (data.credit)
                    defaultHints.credit = "DEFAULT: " + data.credit;
                setHints(defaultHints);
                if (!$('#id_slug').val() && data.headline){
                    $('#id_slug').val(URLify(data.headline));
                }
            });
        } else {
            setHints({
                headline: 'Set the headline of the slide.',
                text: 'Set the text of the slide.',
                caption: 'Set the caption for the media of the slide.',
                credit: 'Set the credit for the media of the slide.'
            });
        }
    }
    $(document).ready(function() {
        getAdapterValues();
        $('#id_content_type').on('change', getAdapterValues);
        $('#id_object_id').on('change', getAdapterValues);
    });

})(django.jQuery);

