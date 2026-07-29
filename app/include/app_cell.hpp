//
//  app_cell.hpp
//  Moonlight
//
//  Created by Даниил Виноградов on 03.06.2021.
//

#pragma once

#include <borealis.hpp>
#include "GameStreamClient.hpp"

class AppCell : public brls::Box {
  public:
    AppCell(const Host& host, const AppInfo& app, int currentApp);

    BRLS_BIND(brls::Image, image, "image");
    BRLS_BIND(brls::Label, title, "title");
    BRLS_BIND(brls::Image, currentAppImage, "current_app_image");
    BRLS_BIND(brls::Image, favoriteAppImage, "favorite_app_image");
    BRLS_BIND(brls::Rectangle, unactiveLayer, "unactive_layer");

    void setFavorite(bool favorite);

  private:
    void updateFavoriteAction(Host host, AppInfo app);
};
