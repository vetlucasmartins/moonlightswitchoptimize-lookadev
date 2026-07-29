//
//  mapping_layout_editor.hpp
//  Moonlight
//
//  Created by Даниил Виноградов on 09.10.2021.
//

#pragma once

#include "utils/Settings.hpp"
#include <borealis.hpp>

class MappingLayoutEditor : public brls::Box {
  public:
    std::function<void(void)> dismissCb;

    MappingLayoutEditor(int layoutNumber, std::function<void(void)> dismissCb);
    ~MappingLayoutEditor();

    brls::View* getParentNavigationDecision(brls::View* from, brls::View* newFocus,
                                           brls::FocusDirection direction) override;
    void dismiss(std::function<void(void)> cb = [] {}) override;

  private:
    int layoutNumber;
    brls::Label* titleLabel;

    void renameLayout();
    void removeLayout();
};
