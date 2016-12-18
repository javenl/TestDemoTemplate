//
//  ViewController.m
//  TestDemo
//
//  Created by liu on 16/12/16.
//  Copyright © 2016年 liu. All rights reserved.
//

#import "ViewController.h"

@interface ActionModel : NSObject

@property (nonatomic, copy) NSString *title;
@property (nonatomic, weak) id target;
@property (nonatomic, assign) SEL action;

@end

@implementation ActionModel

+ (ActionModel *)handleWithTitle:(NSString *)title target:(id)target action:(SEL)action {
    ActionModel *model = [[ActionModel alloc] init];
    model.target = target;
    model.title = title;
    model.action = action;
    return model;
}

- (void)performAction {
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Warc-performSelector-leaks"
    [self.target performSelector:self.action withObject:nil];
#pragma clang diagnostic pop
}

@end

@interface ViewController () <UITableViewDelegate, UITableViewDataSource>

@property (nonatomic, strong) UITableView *tableView;
@property (nonatomic, strong) NSArray *handles;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"Demo";
    
    self.tableView = [[UITableView alloc] initWithFrame:self.view.bounds];
    self.tableView.dataSource = self;
    self.tableView.delegate = self;
    [self.tableView registerClass:[UITableViewCell class] forCellReuseIdentifier:@"UITableViewCell"];
    [self.view addSubview:self.tableView];
    
    self.handles = @[[ActionModel handleWithTitle:@"test1" target:self action:@selector(didTapTest1)],
                     [ActionModel handleWithTitle:@"test2" target:self action:@selector(didTapTest2)],
                     ];
}

#pragma mark - Event

- (void)didTapTest1 {
    NSLog(@"test1");
}

- (void)didTapTest2 {
    NSLog(@"test2");
}

#pragma mark - UITableViewDataSource

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return self.handles.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"UITableViewCell"];
    ActionModel *action = self.handles[indexPath.row];
    cell.textLabel.text = action.title;
    return cell;
}

#pragma mark - UITableViewDelegate

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
    return 44;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    ActionModel *action = self.handles[indexPath.row];
    [action performAction];
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
}

@end
