


########################################################################
class MDLTouch

    #----------------------------------------------------------------------
    constructor: () ->

        @ONSWIPE = false
        @ONMOVING = false
        @DEBUG = false

        @WIDTH_DRAWER = $(".mdl-layout__drawer").width() + parseInt($(".mdl-layout__drawer").css("border-right-width")) + parseInt($(".mdl-layout__drawer").css("border-left-width"))
        @MAX_DISTANCE_DRAWER = @WIDTH_DRAWER*0.4
        @MIN_DISTANCE_DRAWER = 50



    #----------------------------------------------------------------------
    start_pand_drawer: (event) =>
        cls = @

        if event.center.x < cls.MIN_DISTANCE_DRAWER
            cls.ONSWIPE = true
        #else:
            #console.log("No ONSWIPE", event.center.x, cls.MIN_DISTANCE_DRAWER)


    #----------------------------------------------------------------------
    start_pand_layoutdrawer: (event) =>
        cls = @

        if $(".mdl-layout__drawer, .mdl-layout__obfuscator").hasClass("is-visible")
            if event.center.x < cls.WIDTH_DRAWER + cls.MIN_DISTANCE_DRAWER
                cls.ONSWIPE = true




    #----------------------------------------------------------------------
    pand_drawer: (event) =>
        cls = @

        if cls.ONSWIPE

            X = event.center.x - cls.WIDTH_DRAWER


            #if event.center.x < cls.MIN_DISTANCE_DRAWER
                #$(".mdl-layout__drawer, .mdl-layout__obfuscator").removeClass("is-visible")
                #$(".mdl-layout__drawer").css({"-webkit-transition-duration": "0.2s"})
                #$(".mdl-layout__drawer").css({"-webkit-transform": "translateX(-#{cls.WIDTH_DRAWER}px)"})
                ##return

            if X > 0
                $(".mdl-layout__drawer, .mdl-layout__obfuscator").removeClass("is-visible")
                $(".mdl-layout__drawer").css({"-webkit-transition-duration": "0s"})
                $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(0px)"})
                #return

            else
                $(".mdl-layout__drawer, .mdl-layout__obfuscator").addClass("is-visible")
                $(".mdl-layout__drawer").css({"-webkit-transition-duration": "0s"})
                $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(#{X}px)"})



            #loop
              #console.log("animating...")
              #break if $(".mdl-layout__drawer").css("transform") is "matrix(1, 0, 0, 1, #{X}, 0)"


            #loop
              #console.log("animating...")
              #break if $(".mdl-layout__drawer").css("transform") is "matrix(1, 0, 0, 1, -240, 0)"


    #----------------------------------------------------------------------
    swipe_drawer: (event) =>
        cls = @
        swiperight = () ->
            if cls.DEBUG
                console.log("Swipe drawer", cls.ONSWIPE)


            if cls.ONSWIPE and event.center.x > cls.MAX_DISTANCE_DRAWER
                if cls.DEBUG
                    console.log("Drawer visible!")
                cls.ONSWIPE = false
                $(".mdl-layout__drawer, .mdl-layout__obfuscator").addClass("is-visible")
                $(".mdl-layout__drawer").css({"-webkit-transition-duration": "0.2s"})
                $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(0)"})

            else
                if cls.DEBUG
                    console.log("Drawer no visible!")
                cls.ONSWIPE = false
                $(".mdl-layout__drawer, .mdl-layout__obfuscator").removeClass("is-visible")
                $(".mdl-layout__drawer").css({"-webkit-transition-duration": "0.2s"})
                $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(-#{cls.WIDTH_DRAWER}px)"})

        setTimeout(swiperight, 50)


    #----------------------------------------------------------------------
    hide_drawer: (event) =>
        cls = @
        hide_ = () ->
            $(".mdl-layout__drawer, .mdl-layout__obfuscator").removeClass("is-visible")
            $(".mdl-layout__drawer").css({"-webkit-transition-duration": "0s"})
            $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(-#{cls.WIDTH_DRAWER}px)"})
            $(".mdl-layout__drawer-button-menu").fadeIn()
            $(".mdl-layout__drawer-button-home").fadeOut()
        setTimeout(hide_, 1)


$(document).ready ->


    MDLTouch = new MDLTouch()


#Contructor
#----------------------------------------------------------------------

    #var myElement = document.getElementById('myElement');
    MDL_Layout = new Hammer($("body")[0])
    MDL_Layout.get("swipe").set({velocity: 0, pointers: 1})
    MDL_LayoutDrawer = new Hammer($(".mdl-layout__drawer")[0])
    MDL_LayoutDrawer.get("swipe").set({velocity: 0, pointers: 1})

    #layout = $(".mdl-layout")



#----------------------------------------------------------------------



#Events
#----------------------------------------------------------------------

#----------------------------------------------------------------------

    $(document).on "click", ".mdl-layout__obfuscator", (event) ->
        if MDLTouch.DEBUG
            console.log("Click obfuscator")
        $(".mdl-layout__drawer, .mdl-layout__obfuscator").removeClass("is-visible")
        $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(-#{MDLTouch.WIDTH_DRAWER}px)"})


    $(document).on "click", ".mdl-layout__drawer-button", (event) ->
        if MDLTouch.DEBUG
            console.log("Click drawer button")
        if $(".mdl-layout__drawer").hasClass("is-visible")
            $(".mdl-layout__drawer, .mdl-layout__obfuscator").addClass("is-visible")
            $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(0px)"})
        else
            $(".mdl-layout__drawer, .mdl-layout__obfuscator").removeClass("is-visible")
            $(".mdl-layout__drawer").css({"-webkit-transform": "translateX(-#{MDLTouch.WIDTH_DRAWER}px)"})


    $(".mdl-layout__drawer-button-home").on "click", MDLTouch.hide_drawer


    MDL_Layout.on "panright", MDLTouch.start_pand_drawer
    MDL_Layout.on "panright panleft", MDLTouch.pand_drawer
    MDL_Layout.on "swiperight swipeleft", MDLTouch.swipe_drawer


    MDL_Layout.on "panleft", MDLTouch.start_pand_layoutdrawer
    MDL_LayoutDrawer.on "panright panleft", MDLTouch.pand_drawer
    MDL_LayoutDrawer.on "swiperight swipeleft", MDLTouch.swipe_drawer




    #MDL_Layout.on "swiperight swipeleft", MDLTouch.swipe_drawer


    #MDL_LayoutDrawer.on "swipeleft", (event) ->

        #console.log("Swipeleft drawer")

        #if ONSWIPE and event.center.x < 10

            ##if ONSWIPE

            #ONSWIPE = false
            ##$(".mdl-layout__drawer").css({"width": "240px"})
            #$(".mdl-layout__drawer").removeClass("is-visible")
            #$(".mdl-layout__drawer").animate({"-webkit-transform": "translateX(-240px))"})
            ##$(".mdl-layout__drawer-button").click();






