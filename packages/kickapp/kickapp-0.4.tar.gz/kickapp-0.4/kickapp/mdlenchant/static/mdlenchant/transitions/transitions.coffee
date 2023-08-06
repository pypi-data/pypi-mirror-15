

########################################################################

$(document).ready ->

    console.log("Transitions Ready!")



#Contructor
#----------------------------------------------------------------------

    for page in $(".body-page")
        url = $(page).data("load")
        #console.log("Loading #{url}")
        $(page).load("#{url}")

#----------------------------------------------------------------------



    $(document).on "click", "a", (event) ->
        if not $(@).hasClass("no-outpage")
            event.preventDefault()

            url = $(@).data("load")

            if not url
                url = $(@).attr("data-load")


            target = $(".body[data-load='#{url}']")
            #console.log(target)

            $(".body.body-current").css({"-webkit-transition-duration": "0.1s"})
            $(".body.body-current").css({"-webkit-transform": "translateY(100vh)"})
            $(".body").removeClass("body-current")

            show_ = () ->
                target.addClass("body-current")
                target.css({"-webkit-transition-duration": "0.1s"})
                target.css({"-webkit-transform": "translateY(0)"})
            setTimeout(show_, 50)