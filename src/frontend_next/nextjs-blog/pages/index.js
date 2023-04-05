import Head from 'next/head'
import Link from 'next/link';
import React, {useEffect} from "react";
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
    SimpleCell,
    Input,
    FormItem,
    Button,
    FormLayout,
    CustomSelectOption,
    Select,
    Div,
    CardGrid,
    Card,
    Spacing,
    Gradient,
    Snackbar,
} from '@vkontakte/vkui';
import '@vkontakte/vkui/dist/vkui.css';
import {Icon28CheckCircleOutline, Icon28ErrorCircleOutline} from "@vkontakte/icons";

export default function Home() {
    // if (!checkAuth()) {
    //   // redirect to /auth by next
    //   return (
    //       <meta httpEquiv="refresh" content="0; url=/auth" />
    //   )
    // }

    const [snackbar, setSnackbar] = React.useState(null);
    const [user, setUser] = React.useState({});
    const [access_token, setToken] = React.useState('');
    const [teams, setTeams] = React.useState([{}]);
    const [team, setTeam] = React.useState(null);
    const [stage, setStage] = React.useState(null);
    const [_time, setTime] = React.useState(null);

    const secondsToHms = (d) => {
        d = Number(d);
        // return mm:ss with leading zeroes
        return Math.floor(d / 60) + ":" + ("0" + Math.floor(d % 60)).slice(-2);
    }

    const openSuccess = (e) => {
        // if (snackbar) return;
        setSnackbar(
            <Snackbar
                onClose={() => setSnackbar(null)}
                before={<Icon28CheckCircleOutline fill="var(--vkui--color_icon_positive)"/>}
            >
                {e}
            </Snackbar>
        );
    };

    // create async function to calculate estimated time
    const setTimer = async (time) => {
        setTime(time);
        const timer = setInterval(() => {
            if (time <= 0) {
                setTime(null);
                return clearInterval(timer);
            }
            time--;
            document.getElementById('timer').innerHTML = 'Возвращайтесь через: <b>' + secondsToHms(time) + '</b>';
        }, 1000);
    }

    const openError = (e) => {
        // if (snackbar) return;
        setSnackbar(
            <Snackbar
                onClose={() => setSnackbar(null)}
                before={<Icon28ErrorCircleOutline fill="var(--vkui--color_icon_negative)"/>}
            >
                {e}
            </Snackbar>
        );
    };

    const onSubmit = (buttonId) => {
        if (!team) {
            openError("Выберите команду!");
            return;
        }

        fetch('http://85.21.8.81:8000/api/v1/team/' + team + '/join/' + String(user.id), {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            }
        }).then(r => r.json());

        fetch('http://85.21.8.81:8000/api/v1/score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            },
            body: JSON.stringify({
                team_id: Number(team),
                score: Number(buttonId),
                user_id: user.id
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.detail) {
                    openError(
                        data.detail.message +
                        '. Оставшееся время: ' +
                        secondsToHms(data.detail.estimated_time)
                    );

                    if (_time == null) {
                        setTimer(data.detail.estimated_time).then(r => r);
                    }
                } else {
                    openSuccess("Ответ принят!");

                    if (_time == null) {
                        setTimer(600).then(r => r);
                    }
                }
            })
            .catch((error) => {
                openError("Ошибка сервера: " + error)
                console.error('Error:', error);
            });
    }

    // request to /api/v1/users/me, save data to state
    useEffect(() => {
        setToken(sessionStorage.getItem('access_token'));
        getTeams();

        fetch('http://85.21.8.81:8000/api/v1/users/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + sessionStorage.getItem('access_token')
            }
        })
            .then(response => {
                if (response.status === 401) {
                    sessionStorage.removeItem('access_token');
                    window.location.href = '/auth';
                } else {
                    return response.json();
                }
            })
            .then(data => {
                setUser(data);
            })
    }, []);

    const getTeams = () => {
        fetch('http://85.21.8.81:8000/api/v1/stage', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            }
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.stage);
                return data.stage
            }).then(_stage => {
            fetch('http://85.21.8.81:8000/api/v1/teams/' + _stage, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
            })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    console.log(data);
                    setTeams(data);
                });
        })
    }

    return (
        <ConfigProvider platform={"android"} appearance={"light"}>
            <AdaptivityProvider>
                <AppRoot>
                    <SplitLayout style={{marginTop: 0}}>
                        <SplitCol spaced={true}>
                            <View activePanel="main">
                                <Panel id="main">
                                    <PanelHeader>{user.first_name + ' ' + user.last_name}</PanelHeader>
                                    <Group>
                                        <Div>
                                            <p>Пришло время узнать, насколько вы чувствуете <b>сплоченность</b> с
                                                командой.</p>
                                            <p>Выберите на круге тот участок, который наиболее описывает
                                                вашу <b>сплоченность</b> с командой.</p>
                                        </Div>
                                        <FormItem top={team ? "Команда " + team : "Команда не выбрана"}>
                                            <Select
                                                placeholder="Не выбрана"
                                                options={teams.map(_team => ({
                                                    label: "Команда " + _team.id,
                                                    value: _team.id
                                                }))}
                                                onChange={(e) => setTeam(e.target.value)}
                                                status={team ? "valid" : "error"}
                                            />
                                        </FormItem>
                                        {_time && <Div id={"timer"}></Div>}
                                        <Spacing size={16}/>
                                        <CardGrid size="m">
                                            {Array.from({length: 8}).map((_, i) => (
                                                <Card id={String(7 - i)} key={7 - i}
                                                      style={{
                                                          paddingTop: 5,
                                                          paddingBottom: 5,
                                                          background: 'rgb(38,136,235)',
                                                      }}
                                                      onClick={() => onSubmit(7 - i)}
                                                >
                                                    <Div style={{
                                                        textAlign: 'center',
                                                        color: 'white',
                                                    }}>
                                                        {7 - i}
                                                    </Div>
                                                </Card>
                                            ))}
                                        </CardGrid>
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