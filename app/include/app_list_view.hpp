//
//  app_list_view.hpp
//  Moonlight
//
//  Created by Даниил Виноградов on 26.05.2021.
//

#pragma once

#include "app_cell.hpp"
#include "grid_view.hpp"
#include "loading_overlay.hpp"
#include "utils/Settings.hpp"
#include <borealis.hpp>
#include "GameStreamClient.hpp"

#include <optional>

class AppListView : public brls::Box {
  public:
    AppListView(const Host& host);

    void onLayout() override;
    void willAppear(bool resetState) override;

  private:
    Host host;
    brls::View* hintView = nullptr;
    std::optional<AppInfo> currentApp;
    bool loading = false;
    bool inputBlocked = false;
    LoadingOverlay* loader = nullptr;
    void blockInput(bool block);

    GridView* gridView;
    BRLS_BIND(brls::Box, container, "container");

    void setCurrentApp(const AppInfo& app);
    void terninateApp();
    void updateAppList();
    void updateFavoriteAction(AppCell* cell, Host host, const AppInfo& app);
};
