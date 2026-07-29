//
//  button_selecting_dialog.hpp
//  Moonlight
//
//  Created by Даниил Виноградов on 19.07.2021.
//

#pragma once

#include <borealis.hpp>

class ButtonSelectingDialog : public brls::Dialog {
  public:
    ~ButtonSelectingDialog();
    static ButtonSelectingDialog*
    create(std::string titleText,
           std::function<void(std::vector<brls::ControllerButton>)> callback,
           bool oneKey = false);
    void open() override;

  private:
    brls::Animatable timer;
    std::function<void(std::vector<brls::ControllerButton>)> callback;
    std::string titleText;
    std::vector<brls::ControllerButton> buttons;
    brls::ControllerState oldState;
    brls::Label* label;
    bool oneKey;

    ButtonSelectingDialog(
        brls::Box* box, std::function<void(std::vector<brls::ControllerButton>)> callback,
        bool oneKey);

    void reloadLabel();
    std::string buttonsText();

    void draw(NVGcontext* vg, float x, float y, float width, float height,
              brls::Style style, brls::FrameContext* ctx) override;
};
