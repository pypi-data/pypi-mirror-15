





########################################################################
class MDLenchant



    #----------------------------------------------------------------------
    open_link: (url) =>
        cls = @

        $.ajax
            type: "GET"
            url: "/mdlenchant/openlink/"
            data: {"url": url}
            success: (response) ->
                console.log(response.success)





$(document).ready ->

    console.log("MDLenchant Ready!")
    mdlenchant = new MDLenchant()




#Events
#----------------------------------------------------------------------
    #$(".bras-button-play").on "click", api.diagnostic
    #$(".bras-button-play").on "click", animation.first_animation
    #$(".bras-button-stop").on "click", animation.second_animation

#----------------------------------------------------------------------


    $(document).on "click", ".mdle-open-on-browser", (event) ->
        event.preventDefault()

        url = $(@).attr("href")
        mdlenchant.open_link(url)