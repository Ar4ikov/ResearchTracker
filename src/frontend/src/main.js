import React from 'react';
import ReactDOM from 'react-dom';
import {
  AdaptivityProvider,
  ConfigProvider,
  AppRoot,
  SplitLayout,
  SplitCol,
  View,
  Panel,
  PanelHeader,
  Header,
  Group,
  SimpleCell, Input, FormItem, Button, FormLayout,
} from '@vkontakte/vkui';
import '@vkontakte/vkui/dist/vkui.css';


export const MainPage = () => {
  const user = {
    name: 'Василий',
  }

  return (
      <View activePanel="main">
        <Panel id="main">
            <PanelHeader>Василий Пупкин</PanelHeader>
            <Group>
                <SimpleCell>
                    Привет, {user.name}!
                </SimpleCell>
            </Group>
        </Panel>
      </View>
  );
}
