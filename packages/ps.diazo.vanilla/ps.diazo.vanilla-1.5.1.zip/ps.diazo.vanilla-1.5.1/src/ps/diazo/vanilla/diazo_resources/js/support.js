function config_reset_height_listing(listing) {
  var h = ['h3', 'h2', '.item.listing_type', '.item.location', '.item.location_type', '.item.view_type', '.item.lot_size', '.item.object_type'];
  jQuery(listing).children(h).each(function(index) {
    jQuery(this).height('auto');
  });
}


function column_counter(items) {
  my_width = jQuery(items).width();
  my_head_width = jQuery(items).find('.collection-item h2:first').width();
  //find out how many items in one row
  if (my_width > 800) {
    listing_col = 3;
  } else if (my_width > 200) {
    if (my_head_width < 400) {
      listing_col = 2;
    } else {
      listing_col = 1;
    }
  } else if (my_width < 200) {
    listing_col = 1;
  } else {
    listing_col = false;
  }
  return listing_col;
}


function balance_height(items) {
  //get nr. of item columns
  columns = column_counter(items);
  //we have more then 1 column
  if (columns > 1) {
    //set height depending on column nr.
    lastelement = jQuery(items).children('.collection-item').length;
    lastelement = lastelement - 1;
    jQuery(items).children('.collection-item').each(function(index) {
      // Modulo operator to fing begin of each row
      mod = index % columns;
      if (mod < 1) {
        //mod == 0 -> first element in a row
        if (index > 0) {
          balance_item(item0, item1, item2);
          height0 = item0.height();
          if (item1) {
            height1 = item1.height();
          } else {
            height1 = 0;
          }
          if (item2) {
            height2 = item2.height();
          } else {
            height2 = 0;
          }
          row_height = Math.max(height0, height1, height2);
          if (item0) {
            jQuery(item0).height(row_height);
          }
          if (item1) {
            jQuery(item1).height(row_height);
          }
          if (item2) {
            jQuery(item2).height(row_height);
          }
        }
        // remember first row item with the name 'item0'
        item0 = jQuery(this);
        // unset css defaults for calculate real height
        item0.height('auto');
        item0.css('min-height', 'auto');
        item1 = null;
        height1 = 0;
        item2 = null;
        height2 = 0;
      } else {
        if (mod == 1) {
          // remember second row item with the name 'item1'
          // last item when have 2 columns
          item1 = jQuery(this);
          // unset css defaults for calculate real height
          item1.height('auto');
          item1.css('min-height', 'auto');
        }
        if (mod == 2) {
          // remember third row item with the name 'item2'
          // last when have 3 columns
          item2 = jQuery(this);
          // unset css defaults for calculate real height
          item2.height('auto');
          item2.css('min-height', 'auto');
        }
      }

      // For last row
      if (lastelement == index) {
        balance_bedbath(item0, item1, item2);
        balance_item(item0, item1, item2);
        height0 = item0.height();
        if (item1) {
          height1 = item1.height();
        } else {
          height1 = 0;
        }
        if (item2) {
          height2 = item2.height();
        } else {
          height2 = 0;
        }
        row_height = Math.max(height0, height1, height2);
        if (item0) {
          jQuery(item0).height(row_height);
        }
        if (item1) {
          jQuery(item1).height(row_height);
        }
        if (item2) {
          jQuery(item2).height(row_height);
        }
      }
    });
  } else {
    //do nothing
  }
}


function balance_field(name, item0, item1, item2) {
  item_field0 = jQuery(item0).children(name);
  item_field1 = jQuery(item1).children(name);
  item_field2 = jQuery(item2).children(name);
  field_height0 = item_field0.height();
  if (item1) {
    field_height1 = item_field1.height();
  } else {
    field_height1 = 0;
  }
  if (item2) {
    field_height2 = item_field2.height();
  } else {
    field_height2 = 0;
  }
  listing_field_height = Math.max(field_height0, field_height1, field_height2);
  if (item_field0) {
    jQuery(item_field0).height(listing_field_height);
  }
  if (item_field1) {
    jQuery(item_field1).height(listing_field_height);
  }
  if (item_field2) {
    jQuery(item_field2).height(listing_field_height);
  }
}


function balance_bedbath(item0, item1, item2) {
  selector = '.item.beds_baths';
  item_field0 = jQuery(item0).children(selector);
  item_field1 = jQuery(item1).children(selector);
  item_field2 = jQuery(item2).children(selector);
  if (jQuery('.collection-item.tileItem .item.beds_baths').length > 0) {
    next_class = jQuery('.collection-item.tileItem').find(selector).next().attr('class').replace(' ', '.');
    clone = '<div class="item beds_baths">&nbsp;</div>';
    if (item_field0.length > 0 || item_field1.length > 0 || item_field2.length > 0) {
      if (item_field0.length < 1) {
        jQuery(item0).children('.' + next_class).before(clone);
      }
      if (item_field1.length < 1) {
        jQuery(item1).children('.' + next_class).before(clone);
      }
      if (item_field2.length < 1) {
        jQuery(item2).children('.' + next_class).before(clone);
      }
    }
  } else {
    return false;
  }
  // One item have bedbath else return false
  // Find out with item dont have bedbath
  // Prepend this div class to next field
}


function balance_item(item0, item1, item2) {
  balance_bedbath(item0, item1, item2);
  // class title
  balance_field('h2, h3', item0, item1, item2);
  // class item
  balance_field('.item.listing_type', item0, item1, item2);
  balance_field('.item.location', item0, item1, item2);
  balance_field('.item.location_type', item0, item1, item2);
  balance_field('.item.view_type', item0, item1, item2);
  balance_field('.item.lot_size', item0, item1, item2);
  balance_field('.item.object_type', item0, item1, item2);
}


function is_ListingRowPage() {
  //returns true or false if the the page is Listing Summary
  if (jQuery('section.listing-summary').length > 0 && jQuery('section.listing-summary.development-summary').length < 1) {
    return true;
  } else {
    return false;
  }
}


function setup_ListingSummary() {
  // we do this only ONE time and add classes to $(".listing-summary")
  jQuery(".listing-summary").addClass('properties-rows').wrapInner('<div class="row" />');
  //...
}


function is_improvedListing(listing) {
  /* return true if we changed this listing already,  return false if we need to change it */
  if (jQuery(listing).find('.improved').length > 0) {
    return true;
  } else {
    return false;
  }
}


function improve_img_row() {
  jQuery(".property .image .content a").each(function(index) {
    child = jQuery(this).children('img');
    jQuery(this).empty().after(child);
  });
}


function add_class_improvelisting() {
  jQuery(".listing-summary .tileItem").addClass('property').wrapInner('<div class="row" />');
  jQuery(".listing-summary .property figure").addClass('image col-md-3').wrapInner('<div class="content" />');
}


function ajax_improveListing(listing) {
  // changes html of ONE listing
  try {
    dictonary = map_listing_data(jQuery(listing).children('dl'));
  } catch(err) {
    return false;
  }
  jQuery(listing).addClass('improved');

  dictonary.title = jQuery(listing).siblings('.tileHeadline').html();
  dictonary.linktarget = jQuery(listing).parent().find('a:first').attr('href');
  jQuery(listing).siblings('.tileHeadline').remove();
  // clear existing detail structure
  jQuery(listing).empty();
  // set price & title
  jQuery(listing).append('<h1 class="name-of-property">' + dictonary.title + '</h1>');
  // set location
  jQuery(listing).append('<div class="status"><a href="' + dictonary.linktarget + '">' + dictonary.loctype + ' ' + dictonary.propertytype + ' - ' + dictonary.listingtype + '</a></div>');
  jQuery(listing).append('<div class="location"><div class="title"><a href="' + dictonary.linktarget + '">' + dictonary.location + '</a></div></div>');
  jQuery(listing).append('<div class="area"><span class="key" title="Area">&nbsp</span><span class="value">' + dictonary.area + '</span></div>');
  jQuery(listing).append('<div class="price"><p class="value">' + dictonary.price + '</p></div>');
  if (dictonary.type == "house") {
    jQuery(listing).append('<div class="bedbath"><div class="bathrooms"></div><div class="value" title="Bedroom and Bathroom">' + dictonary.bedbath + '</div></div>');
  } else {
    jQuery(listing).append('<div class="locationtype"><span class="key" title="Location Type">&nbsp</span><span class="value">' + dictonary.locationtype + '</span></div>');
  }
}


function improveListing(listing) {
  // changes html of ONE listing
  try {
    dictonary = map_listing_data(jQuery(listing).children('dl'));
  } catch (err) {
    return false;
  }
  jQuery(listing).addClass('improved');

  dictonary.title = jQuery(listing).siblings('.tileHeadline').html();
  dictonary.linktarget = jQuery(listing).parent().find('a:first').attr('href');
  jQuery(listing).siblings('.tileHeadline').remove();
  // clear existing detail structure
  jQuery(listing).empty();
  // set price & title
  jQuery(listing).append('<h1 class="name-of-property">' + dictonary.title + '</h1>');
  //set location
  jQuery(listing).append('<div class="status"><a href="' + dictonary.linktarget + '">' + dictonary.loctype + ' ' + dictonary.propertytype + ' - ' + dictonary.listingtype + '</a></div>');
  jQuery(listing).append('<div class="location"><div class="title"><a href="' + dictonary.linktarget + '">' + dictonary.location + '</a></div></div>');
  if (dictonary.type == "house") {
    jQuery(listing).append('<div class="bedbath"><div class="bathrooms"></div><div class="value" title="Bedroom and Bathroom">' + dictonary.bedbath + '</div></div>');
  } else {
    jQuery(listing).append('<div class="locationtype"><span class="key" title="Location Type">&nbsp</span><span class="value">' + dictonary.locationtype + '</span></div>');
  }
  jQuery(listing).append('<div class="area"><span class="key" title="Area">&nbsp</span><span class="value">' + dictonary.area + '</span></div>');
  jQuery(listing).append('<div class="price"><p class="value">' + dictonary.price + '</p></div>');
}


function enhance_listingbar() {
  /*Improve listing bar*/
  // remove the ugly [ 1 ] notation and give it a class
  jQuery('.listingBar').html(function(i, html) {
    foo = html.replace('[', '<span class="active">').replace(']', '</span>');
    return foo;
  });
}


function map_listing_data(obj) {
  // use data input to give back a easy to access array for mapping
  dict = [];
  new_structure = jQuery(obj).children('div').length > 0;
  if (new_structure) {
    if (obj.find('.listing__beds_baths dd').length > 0) {
      dict.type = 'house';
    } else {
      dict.type = 'land';
    }

    dict.price = obj.find('.listing__price dd').html();
    dict.listingtype = obj.find('.listing__listing_type dd').html();
    dict.propertytype = obj.find('.listing__object_type dd').html();
    dict.location = obj.find('.listing__location dd').html();
    dict.area = obj.find('.listing__lot_size dd').html();
    dict.bedbath = obj.find('.listing__beds_baths dd').html();
    dict.locationtype = obj.find('.listing__location_type dd').html();
    dict.loctype = obj.find('.listing__location_type dd').html();
    if (dict.type == "land") {
      dict.loctype = obj.find('.listing__view_type dd').html();
    }
  } else {
    counter = jQuery(obj).children('dd').length;
    if (counter < 10) {
      dict.type = 'land';
    } else {
      dict.type = 'house';
    }

    dict.price = obj[0].children[1].innerHTML;
    dict.listingtype = obj[0].children[5].innerHTML;
    dict.propertytype = obj[0].children[9].innerHTML;
    dict.loctype = obj[0].children[15].innerHTML;

    if (dict.type == "house") {
      dict.location = obj[0].children[13].innerHTML;
      dict.area = obj[0].children[19].innerHTML;
      dict.bedbath = obj[0].children[11].innerHTML;
      dict.locationtype = obj[0].children[15].innerHTML;
    } else {
      // landlistings have different indexes
      dict.location = obj[0].children[11].innerHTML;
      dict.area = obj[0].children[17].innerHTML;
      dict.bedbath ="";
      dict.locationtype = obj[0].children[13].innerHTML;
    }
  }

  // parse location
  dict.location = parse_location(dict.location);
  return dict;
}


function parse_location(location) {
  // unparsed: San Joaquín, San Joaquín de Flores, Flores, Heredia, Costa Rica
  // parsed: San Joaquín, Heredia, Costa Rica

  try {
    var splitter = location.split(",");
    // react on different location types
    var last = splitter.length - 1;
    var center = splitter.length - 2;
    if (center > 0 && last > 1) {
      location = splitter[0] + "," + splitter[center] + "," + splitter[last];
    }
  } catch(err) {
    // nothing
  }
  return location;
}


function enhance_listiggrid() {
  jQuery(".listing-collection-tile .collection-item .item.location .item-body").each(function(index) {
    mylocation = parse_location(jQuery(this).text());
    jQuery(this).text(mylocation);
  });
  jQuery(".listing-collection-tile .collection-item .item.lot_size").each(function(index) {
    // remove the label of lot size to replace it with css icon
    jQuery(this).children('.item-heading').remove();
    jQuery(this).prepend('<span class="key" title="Area"> </span>');
  });
}


function move_menubar() {
  /*Move menu to under add class "menu-bottom" in body */
  jQuery(".menu-bottom #navigation").insertAfter($("#carousel-wrapper"));
}


function switch_toggle() {
  jQuery("button.navbar-toggle").click(function() {
    jQuery(".navbar-collapse").toggleClass("list-open");
  });
}


function improve_site_social() {
  jQuery(".site-social-switch a").click(function() {
    jQuery(".site-social").toggleClass("site-close");
    jQuery(".site-social-switch a").toggleClass("active");
  });
}


function getDoormatClass() {
  /* Get the existing doormat columns and translate them to the span grid system. */
  var col_class = "";
  if (jQuery('.doormatColumn.column-0').length > 0) {
    // just one column
    col_class = "col-md-12";
  }
  if (jQuery('.doormatColumn.column-1').length > 0) {
    // two columns
    col_class = "col-md-6";
  }
  if (jQuery('.doormatColumn.column-2').length > 0) {
    // three columns
    col_class = "col-md-4";
  }
  if (jQuery('.doormatColumn.column-3').length > 0) {
    // four columns
    col_class = "col-md-3";
  }
  if (jQuery('.doormatColumn.column-4').length > 0) {
    // five columns
    col_class = "";
  }
  if (jQuery('.doormatColumn.column-5').length > 0) {
    // six columns
    col_class = "col-md-2";
  }
  return col_class;
}


function toggle_listing_type() {
  /* Switch Cover page - Listing search */
  jQuery(".listing-search-tile #formfield-form-widgets-jacuzzi span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-jacuzzi label.horizontal").addClass('collapser collapsed');
  jQuery(".listing-search-tile #formfield-form-widgets-pool span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-pool label.horizontal").addClass('collapser collapsed');
  jQuery(".listing-search-tile #formfield-form-widgets-air_condition span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-air_condition label.horizontal").addClass('collapser collapsed');
  jQuery(".listing-search-tile #formfield-form-widgets-view_type span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-view_type label.horizontal").addClass('collapser collapsed');
  jQuery(".listing-search-tile #formfield-form-widgets-location_type span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-location_type label.horizontal").addClass('collapser collapsed');
  jQuery(".listing-search-tile #formfield-form-widgets-geographic_type span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-geographic_type label.horizontal").addClass('collapser collapsed');
  jQuery(".listing-search-tile #formfield-form-widgets-object_type span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-object_type label.horizontal").addClass('collapser collapsed');
  jQuery(".listing-search-tile #formfield-form-widgets-ownership_type span").hide('slow');
  jQuery(".listing-search-tile #formfield-form-widgets-ownership_type label.horizontal").addClass('collapser collapsed');

  jQuery(".listing-search-tile #formfield-form-widgets-air_condition label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-air_condition span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-air_condition label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-air_condition label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-air_condition label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });

  jQuery(".listing-search-tile #formfield-form-widgets-pool label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-pool span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-pool label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-pool label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-pool label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });

  jQuery(".listing-search-tile #formfield-form-widgets-jacuzzi label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-jacuzzi span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-jacuzzi label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-jacuzzi label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-jacuzzi label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });

  jQuery(".listing-search-tile #formfield-form-widgets-view_type label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-view_type span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-view_type label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-view_type label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-view_type label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });

  jQuery(".listing-search-tile #formfield-form-widgets-location_type label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-location_type span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-location_type label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-location_type label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-location_type label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });

  jQuery(".listing-search-tile #formfield-form-widgets-geographic_type label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-geographic_type span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-geographic_type label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-geographic_type label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-geographic_type label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });

  jQuery(".listing-search-tile #formfield-form-widgets-object_type label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-object_type span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-object_type label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-object_type label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-object_type label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });

  jQuery(".listing-search-tile #formfield-form-widgets-ownership_type label.horizontal").click(function() {
    jQuery(".listing-search-tile #formfield-form-widgets-ownership_type span").slideToggle("slow");
    if (jQuery(".listing-search-tile #formfield-form-widgets-ownership_type label.horizontal.collapsed").length > 0) {
      jQuery(".listing-search-tile #formfield-form-widgets-ownership_type label.horizontal.collapsed").removeClass('collapsed').addClass('expanded');
    } else {
      jQuery(".listing-search-tile #formfield-form-widgets-ownership_type label.horizontal.expanded").removeClass('expanded').addClass('collapsed');
    }
  });
}


function class_print_listing(){
  Print = jQuery(".listing.detail p:contains('Print Listing')");
  jQuery(Print).addClass("print-listing");
}


function switch_slider_cover() {
  if (jQuery(".template-layoutedit").length > 0) {
    jQuery(".ps_coverintegrated .tile-name").replaceWith(jQuery(".coverIntegrated"));
  } else {
    jQuery(".ps_coverintegrated").replaceWith(jQuery(".coverIntegrated"));
  }
}


function old_carousel() {
  if (jQuery("#content-header img").length > 0) {
    // nothing
  } else {
    jQuery("#content-header").remove();
  }
}


jQuery(document).ready(function($) {
  old_carousel();
  if (is_ListingRowPage()) {
    // set classes
    setup_ListingSummary();
    //change Listings
    $(".tileItem section").each(function(index) {
      if (!is_improvedListing($(this))) {
        improveListing($(this));
      }
    });
  }
  // only do when we have a listingbar
  if ($('.listingBar').length > 0) {
    enhance_listingbar();
  }

  if ($('.listing-collection-tile .tileItem').length > 0) {
    enhance_listiggrid();
  }

  if ($('.listing.detail').length > 0) {
    class_print_listing();
  }

  improve_site_social();
  switch_toggle();

  if ($(".listing-search-tile.tile-content").length > 0) {
    toggle_listing_type();
  }

  if ($("div.carousel").length > 0) {
    move_menubar();
  }

  if ($(".doormatColumn").length > 0) {
    doormat_col_class = getDoormatClass();
    $("#footer-top-inner .doormatColumn").addClass(doormat_col_class);
  }

  // Ajax Complete
  $( document ).ajaxComplete(function() {
    if (is_ListingRowPage()) {
      // change Listings
      $(".tileItem section:not(.improved)").each(function(index) {
        if (!is_improvedListing($(this))) {
          ajax_improveListing($(this));
        }
      });
    }
  });

  $(window).load(function() {
    if ($('.listing-collection-tile').length > 0) {
      $('.listing-collection-tile').each(function(index) {
        balance_height($(this));
      });
    }
  });

  $(window).resize(function() {
    if ($('.listing-collection-tile').length > 0) {
      $('.listing-collection-tile .collection-item').each(function(index) {
        config_reset_height_listing($(this));
      });
      $('.listing-collection-tile').each(function(index) {
        balance_height($(this));
      });
    }
  });
});
