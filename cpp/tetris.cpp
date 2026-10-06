//Codigo desenvolvido por Jose' Torres

#include <iostream>
#include <windows.h>
#include <conio.h>
#include <string>
#include <random>
#include <vector>
#include <fstream>
#include <sstream>
using namespace std;

//banco de cores
string bc[7] = {"\033[104m","\033[44m","\033[46m","\033[43m","\033[42m","\033[105m","\033[41m"};
//banco de pec,as
int bp[7][4][4][2] = {
	{ {{0,0},{1,0},{2,0},{3,0}}, {{2,-1},{2,0},{2,1},{2,2}}, {{0,1},{1,1},{2,1},{3,1}}, {{1,-1},{1,0},{1,1},{1,2}} },
	{ {{0,0},{0,1},{1,1},{2,1}}, {{1,0},{2,0},{1,1},{1,2}}, {{0,1},{1,1},{2,1},{2,2}}, {{1,0},{1,1},{1,2},{0,2}} },
	{ {{0,1},{1,1},{2,1},{2,0}}, {{1,0},{1,1},{1,2},{2,2}}, {{0,1},{1,1},{2,1},{0,2}}, {{0,0},{1,0},{1,1},{1,2}} },
	{ {{0,0},{1,0},{0,1},{1,1}}, {{0,0},{1,0},{0,1},{1,1}}, {{0,0},{1,0},{0,1},{1,1}}, {{0,0},{1,0},{0,1},{1,1}} },
	{ {{1,0},{2,0},{0,1},{1,1}}, {{1,0},{1,1},{2,1},{2,2}}, {{1,1},{2,1},{0,2},{1,2}}, {{0,0},{0,1},{1,1},{1,2}} },
	{ {{1,0},{0,1},{1,1},{2,1}}, {{1,0},{1,1},{2,1},{1,2}}, {{0,1},{1,1},{2,1},{1,2}}, {{1,0},{0,1},{1,1},{1,2}} },
	{ {{0,0},{1,0},{1,1},{2,1}}, {{2,0},{1,1},{2,1},{1,2}}, {{0,1},{1,1},{1,2},{2,2}}, {{1,0},{0,1},{1,1},{0,2}} },
};
// [0,0] do tabuleiro = [11,9] do terminal ; fim: [0,33]
//mudar barra de lugar
void mb(int x,int y) {
	cout<<"\033["<<y<<";"<<x<<"H";
}
//ler o caracter na posic,ao (x,y)
char lp(int x, int y) {
	mb(x,y);
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFO csbi;
	GetConsoleScreenBufferInfo(hConsole, &csbi);
	COORD cursorPos = csbi.dwCursorPosition;
	char character;
	DWORD charsRead;
	ReadConsoleOutputCharacter(hConsole, &character, 1, cursorPos, &charsRead);
	return character;
}
//escrutura para ll e el
struct CharInfo {
	char character;
	WORD attributes;
};
//ler linha
vector<CharInfo> ll(int line) {
	int startPos=9,endPos=31;
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFO csbi;
	GetConsoleScreenBufferInfo(hConsole, &csbi);
	int width = endPos - startPos -1;
	COORD readPos = {static_cast<SHORT>(startPos), static_cast<SHORT>(line)};
	std::vector<CharInfo> lineContent(width);
	CHAR_INFO buffer[width];
	SMALL_RECT readRegion = {static_cast<SHORT>(startPos), static_cast<SHORT>(line), static_cast<SHORT>(endPos), static_cast<SHORT>(line)};
	ReadConsoleOutput(hConsole, buffer, {static_cast<SHORT>(width), 1}, {0, 0}, &readRegion);
	for (int i = 0; i < width; ++i) {
		lineContent[i].character = buffer[i].Char.AsciiChar;
		lineContent[i].attributes = buffer[i].Attributes;
	}

	return lineContent;
}
//escrever linha
void el(const std::vector<CharInfo>& lineContent) {
	for (const auto& charInfo : lineContent) {
		SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), charInfo.attributes);
		std::cout << charInfo.character;
	}
	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), 7);
}
//verificar movimentos
int vm(int p,int r,int x,int y) {
	for (int d=0; d<4; d++) {
		if(lp(x+bp[p][r][d][0]*2,y+bp[p][r][d][1])!='_') {
			return 0;
		}
	}
	return 1;
}
//desenhar figura
void df(int p,int r,int x,int y,bool apa) {
	for (int d=0; d<4; d++) {
		mb(x+bp[p][r][d][0]*2,y+bp[p][r][d][1]);
		if(apa) {
			cout<<bc[p]<<' ';
		} else {
			cout<<"\033[0m"<<'_';
		}
	}
}

int main() {
	wcout<<"\033[31m   ______\033[38;5;208m ______\033[33m ______\033[32m ____\033[38;5;39m   ____\033[38;5;129m _____\n";
	cout<<"\033[31m  /_  __/\033[38;5;208m/ ____/\033[33m/_  __/\033[32m/ __ \\\033[38;5;39m /  _/\033[38;5;129m/ ___/\n";
	cout<<"\033[31m   / /\033[38;5;208m  / __/\033[33m    / /\033[32m  / /_/ /\033[38;5;39m / /\033[38;5;129m  \\__ \\\n";
	cout<<"\033[31m  / /\033[38;5;208m  / /___\033[33m   / /\033[32m  / _, _/\033[38;5;39m_/ /\033[38;5;129m  ___/ /\n";
	cout<<"\033[31m /_/\033[38;5;208m  /_____/\033[33m  /_/\033[32m  /_/ |_/\033[38;5;39m/___/\033[38;5;129m /____/\n";
	cout<<"          \033[38;5;240m(por Jose' Torres)";
	bool flag3=1;
	while (flag3) {
		mb(0,7);
		cout<<"\33[2K        \033[38;5;44m\033[45mNi'vel:\033[0m 1    \033[38;5;44m\033[45mPontos:\033[0m 0\n";
		//tabuleiro
		cout<<"\33[2K          _ _ _ _ _ _ _ _ _ _ \n";
		for (int i = 0; i < 20; i++)
			cout<<"\33[2K        #|_|_|_|_|_|_|_|_|_|_|#\n";
		cout<<"\33[2K        #######################";
		//comec,ar
		cout<<"\n\33[2K\r\033[92mClique para comec,ar...\033[0m";
		_getch();
		cout << "\33[2K\r";
		int p,r,x,y,pontos=0,niv=1,con=0;
		bool lc;
		while(true) {
			//onde as pec,as sa*o geradas
			x=17;
			y=9;
			random_device dev;
			mt19937 rng(dev());
			uniform_int_distribution<std::mt19937::result_type> dist6(0,6);
			p=dist6(rng); //escolha da pec,a
			r=0; //rotac,ao da pec,a (0 a 3)
			//perdeu
			if(vm(p,r,x,y)==0) {
				sleep(0.6);
				mb(8,7);
				cout << "\033[0m\33[2K\033[38;5;44m\033[45mTabela de classificac,o*es\n";
				cout<<"\033[0m\33[2K\n";
				// Nome do arquivo
				string fn = "Pontuacao_Tetris";
				// Abrir o arquivo para leitura
				ifstream in_l(fn);
				// Usar stringstream para armazenar o conteu'do do arquivo
				stringstream buffer;
				buffer << in_l.rdbuf(); // Le* o conteu'do do arquivo para o buffer
				in_l.close(); // Fechar o arquivo de leitura
				// Agora, trabalhar com o conteu'do do buffer
				string content = buffer.str();
				string modifiedContent;
				string line;
				istringstream input(content);
				// Processar cada linha do conteúdo lido
				bool flag=1,flag2=1;
				int cont=0;
				string esp,nome;
				while (getline(input, line)&&(cont<=20)) {
					if(flag) {
						flag=0;
						esp=line;
					} else {
						flag=1;
						if (pontos>stoi(line)&&(flag2)) {
							flag2=0;
							cout<<"\33[2K\033[0m        -Escreva o seu nome: ";
							cin>>nome;
							mb(0,8+cont);
							cout << "\33[2K\033[0m        - " << nome << '\n';
							cout << "\33[2K\033[0m         Pontos: " << pontos << '\n';
							modifiedContent += nome+"\n"+to_string(pontos)+"\n";
							cont+=2;
						}
						cout << "\33[2K\033[0m        - " << esp << '\n';
						cout << "\33[2K\033[0m         Pontos: " << line << '\n';
						modifiedContent += esp+"\n"+line+"\n";
					}
					cont++;
				}
				cout<<"\33[2K\033[0m\n";
				// Abrir o arquivo para escrita sem truncar
				ofstream in_e(fn, ios::out | ios::trunc);
				// Escrever o conteúdo modificado no arquivo
				in_e << modifiedContent;
				in_e.close(); // Fechar o arquivo de escrita
				cout<<"Quer jogar novamente? (s/n)";
				char soun=_getch();
				if(soun!='s') {
					flag3=0;
				}
				break;
			}
			df(p,r,x,y,1);
			while (true) {
				DWORD start_time = GetTickCount(); // Obte'm o tempo inicial
				while (GetTickCount() - start_time < 200+800/niv) {
					if (_kbhit()) {  // Se uma tecla foi pressionada...
						int key = _getch();  // Captura a tecla pressionada
						// Verifica se a tecla pressionada e' uma tecla especial
						if (key == 224 || key == 0) {
							// Obte'm o segundo valor para identificar a tecla de seta
							key = _getch();
							df(p, r, x, y, 0);
							switch(key) {
								case 77:  // seta para a direita
									x += vm(p, r, x + 2, y) * 2;
									break;
								case 75:  // seta para a esquerda
									x -= vm(p, r, x - 2, y) * 2;
									break;
								case 80:  // seta para baixo
									if(vm(p, r, x, y + 1)) {
										y++;
										pontos++;
										mb(30,7);
										cout<<pontos;
									}
									break;
								case 72:  // seta para cima
									r = (r+vm(p, (r + 1)%4, x, y))%4;
									break;
								default:
									break;
							}
							df(p, r, x, y, 1);
						}
					}
				}
				df(p, r, x, y, 0);
				if(vm(p,r,x,y+1)==0) {
					df(p, r, x, y, 1);
					//encontrar linhas completas
					int b=(p==0&&r==0)?y+1:y+2;
					while(b>=y-1) {
						lc=1; //supor que a linha esta' completa
						for(int a=11; a<=29; a+=2) {
							char po=lp(a,b);
							if(po=='_' || po=='#') {
								lc=0;
							}
						}
						//se a linha estiver completa
						if(lc) {
							//escrever linhas de cima
							for(int n=b; n>=10; n--) {
								mb(10,n);
								vector<CharInfo> li = ll(n-2);
								el(li);
							}
							pontos+=100*niv;
							mb(30,7);
							cout<<pontos;
							con++;
							if(con==10) {
								con=0;
								niv++;
								mb(17,7);
								cout<<niv;
							}
							b++;
						}
						b--;
					}
					break;
				}
				y++;
				df(p, r, x, y, 1);
			}
		}
	}
}