//
//  grid_view.hpp
//  Moonlight
//
//  Created by Даниил Виноградов on 03.06.2021.
//

#pragma once

#include <borealis.hpp>

class GridView : public brls::Box {
  public:
    GridView();
    GridView(int columns);

    void addView(brls::View* view) override;
    void clearViews(bool free = true) override;
    brls::View* getParentNavigationDecision(brls::View* from, brls::View* newFocus,
                                           brls::FocusDirection direction) override;
    std::vector<brls::View*>& getChildren();
    int getItemIndex(brls::View* view);
    int getRows();
    int getItemsInRow(int row);

  private:
    int columls = 1;
    brls::Box* lastContainer = nullptr;
    brls::View* lastView = nullptr;
    std::vector<brls::View*> children;
};
