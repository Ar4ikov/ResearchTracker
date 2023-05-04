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
    SimpleCell, Input, FormItem, Button, FormLayout, Snackbar, CardGrid, Card, CellButton,
} from '@vkontakte/vkui';
import '@vkontakte/vkui/dist/vkui.css';
import React, {useEffect} from "react";
import {Icon28ErrorCircleOutline} from "@vkontakte/icons";

export default function Auth() {
    const hostname = 'http://85.21.8.81:8000';

    const [login, setLogin] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [text, setText] = React.useState('');
    const [token, setToken] = React.useState(null);
    const [snackbar, setSnackbar] = React.useState(null);
    const openError = (e) => {
        if (snackbar) return;
        setSnackbar(
            <Snackbar
                onClose={() => setSnackbar(null)}
                before={<Icon28ErrorCircleOutline fill="var(--vkui--color_icon_negative)"/>}
            >
                {e}
            </Snackbar>,
        );
    };

    const onChange = (e) => {
        const {name, value} = e.currentTarget;

        // check email by regex
        // const isEmail = (email) => {
        //     const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        //     return email === '' ? true : re.test(String(email).toLowerCase());
        // }

        const setStateAction = {
            login: setLogin,
            password: setPassword,
        }[name];

        setStateAction && setStateAction(value);
    };

    const onSubmit = (e) => {
        e.preventDefault();

        if (login === '' || password === '') {
            openError('Заполните все поля');
            return;
        }

        // send request to localhost:8000/api/v1/login OAuth2 endpoint
        // if success, redirect to /profile
        // if fail, show error message

        let details = {
            'username': login,
            'password': password,
            'grant_type': 'password'
        };

        let formBody = [];
        for (let property in details) {
            let encodedKey = encodeURIComponent(property);
            let encodedValue = encodeURIComponent(details[property]);
            formBody.push(encodedKey + "=" + encodedValue);
        }
        formBody = formBody.join("&");

        console.log(formBody);

        fetch(hostname + '/api/v1/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            // body is string
            body: formBody
        })
            .then(response => {
                if (response.status === 401) {
                    console.log('Incorrect credentials');
                    return null;
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data == null) {
                    openError('Неверный логин или пароль');
                    return;
                }

                console.log('Success:', data);

                // set token to sessionStorage
                sessionStorage.setItem('access_token', data.access_token);

                // redirect to /
                window.location.href = '/';

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    useEffect(() => {
        // check auth
        setToken(sessionStorage.getItem('access_token'));
    }, []);

    useEffect(() => {
        if (token != null) {
            window.location.href = '/';
        }
    }, [token]);

    return (
        <ConfigProvider platform="ios" appearance="light">
            <AdaptivityProvider>
                <AppRoot>
                    <SplitLayout style={{marginTop: 150}}>
                        <SplitCol spaced={true}>
                            <View activePanel="login">
                                <Panel id="login">
                                    <PanelHeader>Авторизация</PanelHeader>
                                    <Group>
                                        <Header mode="primary">Бога ради, не вводите здесь свои данные от VK.</Header>
                                        <FormLayout>
                                            <FormItem top="Логин">
                                                <Input type="login" name="login" placeholder="Введите логин"
                                                       onChange={onChange}/>
                                            </FormItem>

                                            <FormItem top="Пароль">
                                                <Input type="password" name="password" placeholder="Введите пароль"
                                                       onChange={onChange}/>
                                            </FormItem>

                                            <FormItem>
                                                <Button size="l" stretched onClick={onSubmit}>
                                                    Вход
                                                </Button>
                                            </FormItem>
                                        </FormLayout>
                                    </Group>
                                    {snackbar}
                                </Panel>
                            </View>
                        </SplitCol>
                    </SplitLayout>
                </AppRoot>
            </AdaptivityProvider>
        </ConfigProvider>
    );
}