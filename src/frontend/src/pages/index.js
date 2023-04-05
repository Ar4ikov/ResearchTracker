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

const AuthForm = () => {
  const [login, setLogin] = React.useState('');
  const [password, setPassword] = React.useState('');

  const onChange = (e) => {
    const { name, value } = e.currentTarget;

    // check email by regex
    const isEmail = (email) => {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return email === '' ? true : re.test(String(email).toLowerCase());
    }

    const setStateAction = {
      login: setLogin,
      password: setPassword,
    }[name];

    // check email
    if (name === 'login') {
        if (isEmail(value)) {
            setStateAction && setStateAction(value);
        } else {
          setStateAction('');
        }

        return;
    }

    setStateAction && setStateAction(value);
  };

  return (
    <View activePanel="login">
      <Panel id="login">
      <PanelHeader>Авторизация</PanelHeader>
        <Group>
          <FormLayout>
            <FormItem top="Логин"
                status={login ? 'valid' : 'error'}
                bottom={login ? 'соси хуй сука' : 'Введите корректный email'}
            >
              <Input type="login" name="login" placeholder="Введите логин" onChange={onChange} />
            </FormItem>

            <FormItem top="Пароль">
              <Input type="password" placeholder="Введите пароль" />
            </FormItem>

            <FormItem>
              <Button size="l" stretched>
                Вход
              </Button>
            </FormItem>
          </FormLayout>
        </Group>
      </Panel>
    </View>
  );
};

ReactDOM.render(
  <ConfigProvider platform="vkcom" appearance="light">
    <AdaptivityProvider>
      <AppRoot>
        <SplitLayout style={{marginTop: 150}}>
          <SplitCol spaced={true}>
            <AuthForm />
          </SplitCol>
        </SplitLayout>
      </AppRoot>
    </AdaptivityProvider>
  </ConfigProvider>,
  document.getElementById('root'),
);